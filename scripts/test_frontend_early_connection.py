import subprocess
import time
import os

def main():
    print("Starting uvicorn...")
    server = subprocess.Popen([r".\\.venv\\Scripts\\uvicorn.exe", "backend.main:app", "--port", "8000"])
    time.sleep(5) # wait for startup
    
    print("Running node frontend_ping.js...")
    res = subprocess.run(["node", "scripts/frontend_ping.js"], capture_output=True, text=True)
    
    report = f"""# Frontend Early Connection Report
## Output
```text
{res.stdout.strip()}
{res.stderr.strip()}
```

## Status
{'PASS' if 'Connection OK' in res.stdout else 'FAIL'}
"""
    os.makedirs("reports", exist_ok=True)
    with open("reports/frontend_connection.md", "w") as f:
        f.write(report)
        
    print("Killing server...")
    server.terminate()
    server.wait()

if __name__ == '__main__':
    main()
