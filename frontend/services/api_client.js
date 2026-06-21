const API_BASE = '/api/v1'; // use relative if proxied or absolute

// Maintain active abort controllers
const activeControllers = new Map();

async function fetchWithRetry(url, options = {}, retries = 1, requestKey = null) {
    const timeout = 5000;
    
    // Abort previous request if same key
    if (requestKey) {
        if (activeControllers.has(requestKey)) {
            activeControllers.get(requestKey).abort();
        }
        activeControllers.set(requestKey, new AbortController());
        options.signal = activeControllers.get(requestKey).signal;
    }
    
    for (let i = 0; i <= retries; i++) {
        let timerId;
        try {
            // Setup timeout signal if not already using one from requestKey
            const controller = options.signal ? null : new AbortController();
            if (controller) {
                timerId = setTimeout(() => controller.abort(), timeout);
                options.signal = controller.signal;
            }
            
            const res = await fetch(url, options);
            if (timerId) clearTimeout(timerId);
            
            if (requestKey) activeControllers.delete(requestKey);
            
            if (!res.ok) {
                const errData = await res.json().catch(()=>({}));
                if (res.status === 422) {
                    const err = new Error("Validasi data gagal: " + JSON.stringify(errData));
                    err.isValidation = true;
                    throw err;
                }
                throw new Error(errData.detail || `HTTP Error ${res.status}`);
            }
            return await res.json();
            
        } catch (err) {
            if (timerId) clearTimeout(timerId);
            
            if (err.name === 'AbortError' && !options.signal?.aborted) {
                // Ignore intentional aborts by user, only retry timeouts
                throw new Error('Request dibatalkan.');
            }
            
            if (err.isValidation || i === retries) throw err;
            await new Promise(r => setTimeout(r, 1000));
        }
    }
}

window.apiClient = {
    health: () => fetchWithRetry(`http://localhost:8000${API_BASE}/health`),
    predict: (data) => fetchWithRetry(`http://localhost:8000${API_BASE}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }, 1, 'predict'),
    explain: (data) => fetchWithRetry(`http://localhost:8000${API_BASE}/explain`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }, 1, 'explain'),
    metadata: () => fetchWithRetry(`http://localhost:8000${API_BASE}/metadata`)
};
