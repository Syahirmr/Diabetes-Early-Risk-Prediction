import asyncio
import httpx
import time
from httpx import AsyncClient

API_URL = "http://localhost:8000/api/v1/predict"

PAYLOAD = {
    "age": 45,
    "gender": "Male",
    "bmi": 24.5,
    "hypertension": 0,
    "heart_disease": 0,
    "smoking_history": "never",
    "hba1c_level": 6.5,
    "blood_glucose_level": 120
}

async def fetch(client):
    start = time.time()
    try:
        response = await client.post(API_URL, json=PAYLOAD)
        latency = time.time() - start
        return response.status_code, latency
    except Exception as e:
        return 500, time.time() - start

async def main():
    print("Starting Stress Test: 50 concurrent requests...")
    start_total = time.time()
    async with AsyncClient() as client:
        tasks = [fetch(client) for _ in range(50)]
        results = await asyncio.gather(*tasks)
    
    end_total = time.time()
    latencies = [r[1] for r in results]
    status_codes = [r[0] for r in results]
    
    avg_latency = sum(latencies) / len(latencies)
    max_latency = max(latencies)
    success_count = status_codes.count(200)
    
    print("\n--- STRESS TEST REPORT ---")
    print(f"Total Requests: 50")
    print(f"Successful Requests (200 OK): {success_count}/50")
    print(f"Failed Requests: {50 - success_count}/50")
    print(f"Average Latency per Request: {avg_latency:.4f} seconds")
    print(f"Max Latency: {max_latency:.4f} seconds")
    print(f"Total Execution Time: {end_total - start_total:.4f} seconds")
    
    if success_count == 50 and avg_latency < 3.0:
        print("\nSTATUS: PASS (SLA < 3 sec met, no 500 errors)")
    else:
        print("\nSTATUS: FAIL")

if __name__ == "__main__":
    asyncio.run(main())
