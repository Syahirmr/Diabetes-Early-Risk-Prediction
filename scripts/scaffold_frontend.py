import os

files = {
    "package.json": """{
  "name": "uas_machinelearning_diabetes",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite frontend --port 3000"
  },
  "devDependencies": {
    "vite": "^5.0.0"
  }
}""",
    "frontend/index.html": """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diabetes Early Risk Prediction</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.x.x/dist/cdn.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <script type="module" src="/main.js"></script>
    <style>
        [x-cloak] { display: none !important; }
        .glass-panel { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); }
    </style>
</head>
<body class="bg-gray-50 text-gray-800 font-sans min-h-screen flex flex-col antialiased">
    <div x-data="appStore" class="flex-grow flex flex-col">
        <!-- Toast Error -->
        <div x-show="error" x-cloak class="fixed top-4 right-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded z-50">
            <span class="block sm:inline" x-text="error"></span>
            <button @click="error = null" class="absolute top-0 bottom-0 right-0 px-4 py-3">&times;</button>
        </div>
        
        <!-- Header -->
        <header class="bg-white shadow-sm border-b">
            <div class="max-w-5xl mx-auto px-4 py-4 flex justify-between items-center">
                <h1 class="text-xl font-bold text-blue-600 flex items-center gap-2 cursor-pointer" @click="goTo('landing')">
                    <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a8 8 0 100 16 8 8 0 000-16zM8.7 13.3a1 1 0 01-1.4 0l-2-2a1 1 0 111.4-1.4l1.3 1.3 4.3-4.3a1 1 0 111.4 1.4l-5 5z"/></svg>
                    Diabetes Risk Platform
                </h1>
                <div class="flex items-center gap-2 text-sm">
                    <span class="w-3 h-3 rounded-full" :class="apiStatus === 'ok' ? 'bg-green-500' : (apiStatus === 'error' ? 'bg-red-500' : 'bg-yellow-500')"></span>
                    <span x-text="apiStatus === 'ok' ? 'System Online' : (apiStatus === 'error' ? 'System Offline' : 'Connecting...')" class="text-gray-500"></span>
                </div>
            </div>
        </header>

        <!-- Pages Router -->
        <main class="flex-grow max-w-5xl mx-auto w-full p-4 sm:p-6">
            <template x-if="step === 'landing'">
                <div x-html="pages.landing"></div>
            </template>
            <template x-if="step === 'assessment'">
                <div x-html="pages.assessment"></div>
            </template>
            <template x-if="step === 'result'">
                <div x-html="pages.result"></div>
            </template>
        </main>
        
        <footer class="bg-gray-100 border-t py-6 text-center text-gray-500 text-sm mt-auto print:hidden">
            <p>&copy; 2026 Diabetes Early Risk Prediction Platform. Bukan alat diagnostik medis.</p>
        </footer>
    </div>
</body>
</html>
""",
    "frontend/main.js": """import './services/api_client.js';
import './store/app_store.js';
import './app.js';
""",
    "frontend/app.js": """// App initialized
""",
    "frontend/store/app_store.js": """document.addEventListener('alpine:init', () => {
    Alpine.data('appStore', () => ({
        step: 'landing', // landing, assessment, result
        apiStatus: 'checking',
        loading: false,
        error: null,
        
        assessment: {
            age: '',
            gender: '',
            bmi: '',
            hypertension: '',
            heart_disease: '',
            smoking_history: '',
            hba1c_level: '',
            blood_glucose_level: ''
        },
        
        resultData: null,
        explainData: null,
        explainLoading: false,
        
        pages: {
            landing: '',
            assessment: '',
            result: ''
        },
        
        components: {
            explanation: ''
        },

        async init() {
            // Load templates
            this.pages.landing = await (await fetch('/pages/landing.html')).text();
            this.pages.assessment = await (await fetch('/pages/assessment.html')).text();
            this.pages.result = await (await fetch('/pages/result.html')).text();
            this.components.explanation = await (await fetch('/components/explanation_panel.html')).text();
            
            // Check API Health
            try {
                await window.apiClient.health();
                this.apiStatus = 'ok';
            } catch(e) {
                this.apiStatus = 'error';
                this.error = "Gagal terhubung ke server backend.";
            }

            // Restore state if any popstate
            window.addEventListener('popstate', (e) => {
                if(e.state && e.state.step) {
                    this.step = e.state.step;
                }
            });
            history.replaceState({step: this.step}, '', '/');
        },
        
        goTo(newStep) {
            this.step = newStep;
            history.pushState({step: newStep}, '', '/' + (newStep === 'landing' ? '' : '#' + newStep));
            window.scrollTo(0,0);
        },
        
        async submitAssessment() {
            this.loading = true;
            this.error = null;
            this.explainData = null; // reset explanation
            
            const payload = {
                age: Number(this.assessment.age),
                gender: this.assessment.gender,
                bmi: Number(this.assessment.bmi),
                hypertension: Number(this.assessment.hypertension),
                heart_disease: Number(this.assessment.heart_disease),
                smoking_history: this.assessment.smoking_history,
                hba1c_level: Number(this.assessment.hba1c_level),
                blood_glucose_level: Number(this.assessment.blood_glucose_level)
            };
            
            try {
                this.resultData = await window.apiClient.predict(payload);
                this.goTo('result');
            } catch(e) {
                this.error = e.message;
            } finally {
                this.loading = false;
            }
        },
        
        async loadExplain() {
            if (this.explainData || this.explainLoading) return;
            this.explainLoading = true;
            const payload = {
                age: Number(this.assessment.age),
                gender: this.assessment.gender,
                bmi: Number(this.assessment.bmi),
                hypertension: Number(this.assessment.hypertension),
                heart_disease: Number(this.assessment.heart_disease),
                smoking_history: this.assessment.smoking_history,
                hba1c_level: Number(this.assessment.hba1c_level),
                blood_glucose_level: Number(this.assessment.blood_glucose_level)
            };
            try {
                this.explainData = await window.apiClient.explain(payload);
            } catch(e) {
                this.error = "Gagal memuat explainability: " + e.message;
            } finally {
                this.explainLoading = false;
            }
        },
        
        printResult() {
            window.print();
        }
    }));
});
""",
    "frontend/services/api_client.js": """const API_BASE = 'http://localhost:8000/api/v1';

async function fetchWithRetry(url, options = {}, retries = 2) {
    const timeout = 5000;
    
    for (let i = 0; i <= retries; i++) {
        try {
            const controller = new AbortController();
            const id = setTimeout(() => controller.abort(), timeout);
            const res = await fetch(url, { ...options, signal: controller.signal });
            clearTimeout(id);
            
            if (!res.ok) {
                const errData = await res.json().catch(()=>({}));
                if (res.status === 422) {
                    throw new Error("Validasi data gagal: " + JSON.stringify(errData));
                }
                throw new Error(errData.detail || `HTTP Error ${res.status}`);
            }
            return await res.json();
        } catch (err) {
            if (i === retries) throw err;
            await new Promise(r => setTimeout(r, 1000));
        }
    }
}

window.apiClient = {
    health: () => fetchWithRetry(`${API_BASE}/health`),
    predict: (data) => fetchWithRetry(`${API_BASE}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }),
    explain: (data) => fetchWithRetry(`${API_BASE}/explain`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }),
    metadata: () => fetchWithRetry(`${API_BASE}/metadata`)
};
""",
    "frontend/pages/landing.html": """<div class="glass-panel rounded-2xl p-8 max-w-4xl mx-auto shadow-xl text-center space-y-6 mt-10">
    <div class="w-20 h-20 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
    </div>
    <h2 class="text-4xl font-extrabold text-gray-900 tracking-tight">Ketahui Risiko Diabetes Sejak Dini</h2>
    <p class="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
        Platform cerdas berbasis Machine Learning untuk membantu mengidentifikasi potensi risiko diabetes berdasarkan gaya hidup dan parameter klinis Anda secara real-time.
    </p>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 my-10 text-left">
        <div class="bg-white p-5 rounded-xl border shadow-sm">
            <h3 class="font-bold text-gray-800">1. Isi Profil</h3>
            <p class="text-sm text-gray-500 mt-2">Lengkapi data dasar usia, BMI, dan kebiasaan sehari-hari.</p>
        </div>
        <div class="bg-white p-5 rounded-xl border shadow-sm">
            <h3 class="font-bold text-gray-800">2. Data Klinis</h3>
            <p class="text-sm text-gray-500 mt-2">Masukkan nilai HbA1c dan Gula Darah dengan aman.</p>
        </div>
        <div class="bg-white p-5 rounded-xl border shadow-sm">
            <h3 class="font-bold text-gray-800">3. Hasil Analisis</h3>
            <p class="text-sm text-gray-500 mt-2">Dapatkan ringkasan tingkat risiko tanpa basa-basi medis.</p>
        </div>
    </div>

    <button @click="goTo('assessment')" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-10 rounded-full transition transform hover:scale-105 shadow-lg text-lg">
        Mulai Asesmen Gratis
    </button>
    
    <div class="mt-8 pt-6 border-t text-sm text-gray-400">
        <strong>Disclaimer:</strong> Hasil prediksi ini bukan diagnosis medis. Konsultasikan ke dokter untuk pemeriksaan klinis.
    </div>
</div>
""",
    "frontend/pages/assessment.html": """<div class="max-w-3xl mx-auto" x-data="{ formStep: 1 }">
    <!-- Progress Bar -->
    <div class="mb-8">
        <div class="flex justify-between text-sm font-medium text-gray-500 mb-2">
            <span :class="formStep >= 1 ? 'text-blue-600' : ''">Profil Dasar</span>
            <span :class="formStep >= 2 ? 'text-blue-600' : ''">Riwayat Penyakit</span>
            <span :class="formStep >= 3 ? 'text-blue-600' : ''">Klinis</span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="bg-blue-600 h-2 rounded-full transition-all duration-300" :style="`width: ${(formStep/3)*100}%`"></div>
        </div>
    </div>

    <div class="bg-white shadow-lg rounded-2xl p-8 border">
        
        <!-- Step 1 -->
        <div x-show="formStep === 1">
            <h3 class="text-2xl font-bold mb-6">Profil Dasar</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Usia (Tahun)</label>
                    <input type="number" x-model="assessment.age" class="w-full p-3 border rounded-lg focus:ring focus:ring-blue-200 focus:border-blue-500" placeholder="Contoh: 45">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Jenis Kelamin</label>
                    <select x-model="assessment.gender" class="w-full p-3 border rounded-lg focus:ring focus:ring-blue-200">
                        <option value="">Pilih...</option>
                        <option value="Male">Laki-laki</option>
                        <option value="Female">Perempuan</option>
                        <option value="Other">Lainnya</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">BMI (Body Mass Index)</label>
                    <input type="number" step="0.1" x-model="assessment.bmi" class="w-full p-3 border rounded-lg" placeholder="Contoh: 24.5">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Status Merokok</label>
                    <select x-model="assessment.smoking_history" class="w-full p-3 border rounded-lg">
                        <option value="">Pilih...</option>
                        <option value="never">Tidak Pernah</option>
                        <option value="current">Perokok Aktif</option>
                        <option value="former">Mantan Perokok</option>
                        <option value="No Info">Tidak Tahu / Lainnya</option>
                    </select>
                </div>
            </div>
            <div class="mt-8 flex justify-end">
                <button @click="if(assessment.age && assessment.gender && assessment.bmi && assessment.smoking_history) formStep = 2" 
                        :disabled="!(assessment.age && assessment.gender && assessment.bmi && assessment.smoking_history)"
                        class="bg-blue-600 disabled:bg-gray-300 text-white px-8 py-3 rounded-lg font-medium transition">Selanjutnya</button>
            </div>
        </div>

        <!-- Step 2 -->
        <div x-show="formStep === 2" x-cloak>
            <h3 class="text-2xl font-bold mb-6">Riwayat Penyakit</h3>
            <div class="space-y-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Riwayat Hipertensi?</label>
                    <div class="flex gap-4">
                        <label class="flex items-center gap-2 p-4 border rounded-lg flex-1 cursor-pointer" :class="assessment.hypertension === '1' ? 'border-blue-500 bg-blue-50' : ''">
                            <input type="radio" name="hyp" value="1" x-model="assessment.hypertension" class="hidden">
                            <div class="w-5 h-5 rounded-full border-2 flex items-center justify-center" :class="assessment.hypertension === '1' ? 'border-blue-500' : 'border-gray-300'">
                                <div class="w-3 h-3 rounded-full bg-blue-500" x-show="assessment.hypertension === '1'"></div>
                            </div>
                            <span>Ya</span>
                        </label>
                        <label class="flex items-center gap-2 p-4 border rounded-lg flex-1 cursor-pointer" :class="assessment.hypertension === '0' ? 'border-blue-500 bg-blue-50' : ''">
                            <input type="radio" name="hyp" value="0" x-model="assessment.hypertension" class="hidden">
                            <div class="w-5 h-5 rounded-full border-2 flex items-center justify-center" :class="assessment.hypertension === '0' ? 'border-blue-500' : 'border-gray-300'">
                                <div class="w-3 h-3 rounded-full bg-blue-500" x-show="assessment.hypertension === '0'"></div>
                            </div>
                            <span>Tidak</span>
                        </label>
                    </div>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Riwayat Penyakit Jantung?</label>
                    <div class="flex gap-4">
                        <label class="flex items-center gap-2 p-4 border rounded-lg flex-1 cursor-pointer" :class="assessment.heart_disease === '1' ? 'border-blue-500 bg-blue-50' : ''">
                            <input type="radio" name="hd" value="1" x-model="assessment.heart_disease" class="hidden">
                            <div class="w-5 h-5 rounded-full border-2 flex items-center justify-center" :class="assessment.heart_disease === '1' ? 'border-blue-500' : 'border-gray-300'">
                                <div class="w-3 h-3 rounded-full bg-blue-500" x-show="assessment.heart_disease === '1'"></div>
                            </div>
                            <span>Ya</span>
                        </label>
                        <label class="flex items-center gap-2 p-4 border rounded-lg flex-1 cursor-pointer" :class="assessment.heart_disease === '0' ? 'border-blue-500 bg-blue-50' : ''">
                            <input type="radio" name="hd" value="0" x-model="assessment.heart_disease" class="hidden">
                            <div class="w-5 h-5 rounded-full border-2 flex items-center justify-center" :class="assessment.heart_disease === '0' ? 'border-blue-500' : 'border-gray-300'">
                                <div class="w-3 h-3 rounded-full bg-blue-500" x-show="assessment.heart_disease === '0'"></div>
                            </div>
                            <span>Tidak</span>
                        </label>
                    </div>
                </div>
            </div>
            <div class="mt-8 flex justify-between">
                <button @click="formStep = 1" class="text-gray-600 px-6 py-3 hover:bg-gray-100 rounded-lg transition">Kembali</button>
                <button @click="if(assessment.hypertension !== '' && assessment.heart_disease !== '') formStep = 3" 
                        :disabled="assessment.hypertension === '' || assessment.heart_disease === ''"
                        class="bg-blue-600 disabled:bg-gray-300 text-white px-8 py-3 rounded-lg font-medium transition">Selanjutnya</button>
            </div>
        </div>

        <!-- Step 3 -->
        <div x-show="formStep === 3" x-cloak>
            <h3 class="text-2xl font-bold mb-6">Parameter Klinis</h3>
            <div class="space-y-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Tingkat HbA1c (%)</label>
                    <input type="number" step="0.1" x-model="assessment.hba1c_level" class="w-full p-3 border rounded-lg" placeholder="Contoh: 6.5">
                    <p class="text-xs text-gray-500 mt-1">Normal: &lt;5.7%</p>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Gula Darah (mg/dL)</label>
                    <input type="number" step="1" x-model="assessment.blood_glucose_level" class="w-full p-3 border rounded-lg" placeholder="Contoh: 120">
                    <p class="text-xs text-gray-500 mt-1">Gula Darah Puasa / Acak.</p>
                </div>
            </div>
            <div class="mt-8 flex justify-between">
                <button @click="formStep = 2" class="text-gray-600 px-6 py-3 hover:bg-gray-100 rounded-lg transition">Kembali</button>
                <button @click="submitAssessment()" 
                        :disabled="!(assessment.hba1c_level && assessment.blood_glucose_level) || loading"
                        class="bg-green-600 disabled:bg-gray-300 text-white px-8 py-3 rounded-lg font-medium transition flex items-center gap-2">
                    <span x-show="!loading">Lihat Hasil Risiko</span>
                    <span x-show="loading" class="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></span>
                </button>
            </div>
        </div>

    </div>
</div>
""",
    "frontend/pages/result.html": """<div class="max-w-4xl mx-auto print:max-w-none print:m-0" x-data="{ expanded: false }">
    <div class="bg-white rounded-2xl shadow-xl overflow-hidden border">
        
        <!-- Header / Banner -->
        <div class="p-8 text-center print:border-b" :class="{
            'bg-red-50 text-red-900': resultData?.risk_level === 'Tinggi',
            'bg-green-50 text-green-900': resultData?.risk_level === 'Rendah'
        }">
            <h2 class="text-sm font-bold uppercase tracking-widest opacity-80 mb-2">Hasil Analisis Risiko</h2>
            <div class="inline-flex items-center justify-center gap-3">
                <span class="text-5xl font-extrabold" x-text="resultData?.risk_level"></span>
                <!-- Gauge Icon -->
                <svg x-show="resultData?.risk_level === 'Tinggi'" class="w-12 h-12 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                <svg x-show="resultData?.risk_level === 'Rendah'" class="w-12 h-12 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </div>
            <p class="mt-4 text-lg max-w-2xl mx-auto" x-text="resultData?.summary"></p>
        </div>

        <div class="p-8 print:p-4">
            
            <div class="mb-8">
                <h3 class="text-xl font-bold mb-3 border-b pb-2">Rekomendasi</h3>
                <p class="text-gray-700 leading-relaxed" x-text="resultData?.recommendation"></p>
            </div>

            <!-- Faktor Utama (Predict endpoint Top 5) -->
            <div class="mb-8 bg-gray-50 rounded-xl p-6 border">
                <h3 class="font-bold text-gray-800 mb-4">Faktor Utama yang Mempengaruhi Risiko</h3>
                <ul class="space-y-3">
                    <template x-for="factor in resultData?.top_factors">
                        <li class="flex items-start gap-3">
                            <span class="mt-1" :class="factor.direction === 'increase' ? 'text-red-500' : 'text-green-500'">
                                <svg x-show="factor.direction === 'increase'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"></path></svg>
                                <svg x-show="factor.direction === 'decrease'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path></svg>
                            </span>
                            <div>
                                <strong class="capitalize" x-text="factor.feature.replace(/_/g, ' ')"></strong>
                                <p class="text-sm text-gray-600" x-text="factor.impact"></p>
                            </div>
                        </li>
                    </template>
                </ul>
            </div>

            <div class="flex flex-col md:flex-row justify-between items-center print:hidden border-t pt-6 mt-6 gap-4">
                <button @click="goTo('assessment')" class="text-gray-500 hover:text-gray-800 font-medium transition">Ulangi Asesmen</button>
                <div class="flex flex-col sm:flex-row gap-4 w-full md:w-auto">
                    <button @click="printResult()" class="flex-1 sm:flex-none flex justify-center items-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-800 px-6 py-2 rounded-lg font-medium transition">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path></svg>
                        Cetak/PDF
                    </button>
                    <button @click="expanded = !expanded; if(expanded) loadExplain();" class="flex-1 sm:flex-none flex justify-center items-center gap-2 bg-blue-50 text-blue-700 px-6 py-2 rounded-lg font-medium hover:bg-blue-100 transition">
                        Analisis Mendalam (Explain)
                        <svg class="w-5 h-5 transform transition-transform" :class="expanded ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </button>
                </div>
            </div>

            <!-- Layer 2: Explainability -->
            <div x-show="expanded" x-collapse class="mt-6 border-t pt-6" x-html="components.explanation"></div>

            <div class="mt-8 text-xs text-gray-400 text-center">
                <span x-text="resultData?.disclaimer"></span>
                <br>
                Dicetak pada: <span x-text="new Date().toLocaleString()"></span>
            </div>
        </div>
    </div>
</div>
""",
    "frontend/components/explanation_panel.html": """<div>
    <h3 class="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
        <svg class="w-6 h-6 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path></svg>
        Explainability Analysis
    </h3>
    
    <!-- Loading Skeleton -->
    <div x-show="explainLoading" class="animate-pulse space-y-4">
        <div class="h-4 bg-gray-200 rounded w-3/4"></div>
        <div class="h-4 bg-gray-200 rounded w-1/2"></div>
        <div class="h-4 bg-gray-200 rounded w-5/6"></div>
    </div>

    <!-- Content -->
    <div x-show="!explainLoading && explainData" class="space-y-4">
        <p class="text-sm text-gray-600 leading-relaxed bg-indigo-50 p-4 rounded-lg border border-indigo-100" x-text="explainData?.explainability_summary"></p>
        
        <h4 class="font-semibold text-sm text-gray-700 mt-6 mb-2">Seluruh Faktor Signifikan</h4>
        <div class="overflow-x-auto border rounded-lg shadow-sm">
            <table class="min-w-full divide-y divide-gray-200 text-sm">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-4 py-3 text-left font-medium text-gray-500">Parameter Klinis</th>
                        <th class="px-4 py-3 text-left font-medium text-gray-500">Dampak</th>
                        <th class="px-4 py-3 text-left font-medium text-gray-500">Keterangan</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <template x-for="f in explainData?.top_factors">
                        <tr>
                            <td class="px-4 py-3 font-medium text-gray-800 capitalize" x-text="f.feature.replace(/_/g, ' ')"></td>
                            <td class="px-4 py-3">
                                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
                                      :class="f.direction === 'increase' ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'">
                                    <span x-text="f.direction === 'increase' ? 'Meningkatkan' : 'Menurunkan'"></span>
                                </span>
                            </td>
                            <td class="px-4 py-3 text-gray-600" x-text="f.impact"></td>
                        </tr>
                    </template>
                </tbody>
            </table>
        </div>
    </div>
</div>
""",
    "scripts/frontend_ping.js": """async function check() {
    try {
        console.log("Pinging health endpoint...");
        const res = await fetch("http://localhost:8000/api/v1/health");
        console.log("Health Status:", res.status, await res.json());

        console.log("\\nPinging predict endpoint...");
        const pRes = await fetch("http://localhost:8000/api/v1/predict", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                age: 50, gender: "Male", bmi: 25, hypertension: 0, heart_disease: 0,
                smoking_history: "never", hba1c_level: 6, blood_glucose_level: 120
            })
        });
        console.log("Predict Status:", pRes.status, await pRes.json());
        
        console.log("\\nPinging predict endpoint (422 test)...");
        const eRes = await fetch("http://localhost:8000/api/v1/predict", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ age: -50 })
        });
        console.log("Error 422 Status:", eRes.status, await eRes.json());
        
        console.log("\\nConnection OK.");
    } catch(e) {
        console.error("Connection Failed:", e);
    }
}
check();
"""
}

import os

os.makedirs("frontend/pages", exist_ok=True)
os.makedirs("frontend/components", exist_ok=True)
os.makedirs("frontend/store", exist_ok=True)
os.makedirs("frontend/services", exist_ok=True)
os.makedirs("scripts", exist_ok=True)

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Scaffold complete.")
