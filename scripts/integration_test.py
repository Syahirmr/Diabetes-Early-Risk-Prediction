import subprocess
import time
import os

def main():
    # Write node script
    node_script = """
fetch("http://localhost:8000/api/v1/health")
    .then(r=>r.json())
    .then(console.log)
    .catch(console.error);
    """
    with open("test_fetch.js", "w") as f:
        f.write(node_script)
        
    print("Starting uvicorn...")
    server = subprocess.Popen([r".\\.venv\\Scripts\\uvicorn.exe", "backend.main:app", "--port", "8000"])
    time.sleep(5) # wait for startup
    
    report = "# Integration Report\n\n"
    
    # 1. curl health
    print("Running curl health...")
    res1 = subprocess.run(["curl", "-s", "http://localhost:8000/api/v1/health"], capture_output=True, text=True)
    report += "## 1. cURL /health\n"
    report += f"```json\n{res1.stdout}\n```\n\n"
    
    # 2. node fetch
    print("Running node fetch...")
    res2 = subprocess.run(["node", "test_fetch.js"], capture_output=True, text=True)
    report += "## 2. Browser Fetch Simulation (Node.js)\n"
    report += f"```javascript\n{res2.stdout}\n```\n\n"
    
    # 3. OPTIONS
    print("Running curl OPTIONS...")
    res3 = subprocess.run(["curl", "-s", "-i", "-X", "OPTIONS", "http://localhost:8000/api/v1/predict", "-H", "Origin: http://localhost:3000", "-H", "Access-Control-Request-Method: POST"], capture_output=True, text=True)
    report += "## 3. cURL OPTIONS Preflight\n"
    report += f"```http\n{res3.stdout}\n```\n\n"
    
    with open("reports/integration_report.md", "w") as f:
        f.write(report)
        
    print("Killing server...")
    server.terminate()
    server.wait()
    
    if os.path.exists("test_fetch.js"):
        os.remove("test_fetch.js")

if __name__ == '__main__':
    main()
