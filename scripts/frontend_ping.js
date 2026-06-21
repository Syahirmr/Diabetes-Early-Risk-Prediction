async function check() {
    try {
        console.log("Pinging health endpoint...");
        const res = await fetch("http://localhost:8000/api/v1/health");
        console.log("Health Status:", res.status, await res.json());

        console.log("\nPinging predict endpoint...");
        const pRes = await fetch("http://localhost:8000/api/v1/predict", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                age: 50, gender: "Male", bmi: 25, hypertension: 0, heart_disease: 0,
                smoking_history: "never", hba1c_level: 6, blood_glucose_level: 120
            })
        });
        console.log("Predict Status:", pRes.status, await pRes.json());
        
        console.log("\nPinging predict endpoint (422 test)...");
        const eRes = await fetch("http://localhost:8000/api/v1/predict", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ age: -50 })
        });
        console.log("Error 422 Status:", eRes.status, await eRes.json());
        
        console.log("\nConnection OK.");
    } catch(e) {
        console.error("Connection Failed:", e);
    }
}
check();
