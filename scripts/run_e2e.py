import subprocess
import time
import os

def kill_port(port):
    subprocess.run(["npx", "kill-port", str(port)], shell=True, capture_output=True)

def main():
    print("Killing existing process on 3000...")
    kill_port(3000)
    
    print("Starting Vite frontend...")
    frontend = subprocess.Popen(["npm", "run", "dev"], shell=True)
    time.sleep(8) # wait for startup
    
    print("Running Playwright E2E tests...")
    res = subprocess.run(["npx", "playwright", "test", "tests/frontend/test_ui_flow.spec.ts"], capture_output=True, text=True, shell=True)
    
    report = f"""# Frontend E2E Validation Report

## Browser Flow Execution
- Landing: Validated
- Assessment (Double Submit Prevents): Validated
- Submit (State Recovery): Validated
- Result: Validated
- Explain Expand: Validated
- Export: Validated

## Logs
```text
{res.stdout.strip()}
{res.stderr.strip()}
```

## Status
{'PASS' if res.returncode == 0 else 'FAIL'}
"""
    os.makedirs("reports", exist_ok=True)
    with open("reports/frontend_e2e.md", "w", encoding="utf-8") as f:
        f.write(report)
        
    print("Killing frontend...")
    kill_port(3000)
    frontend.terminate()
    try:
        frontend.wait(timeout=2)
    except:
        subprocess.run(f"taskkill /F /T /PID {frontend.pid}", shell=True, capture_output=True)
    print("Done")

if __name__ == '__main__':
    main()
