import subprocess
import shutil

def test_real_startup_failfast():
    model_path = "models/artifacts/model.pkl"
    backup_path = "models/artifacts/model.pkl.bak"
    
    # Rename
    shutil.move(model_path, backup_path)
    
    try:
        # Run uvicorn
        process = subprocess.run(
            [r".\\.venv\\Scripts\\uvicorn.exe", "backend.main:app"],
            capture_output=True,
            text=True,
            timeout=15
        )
        assert process.returncode != 0
        
        report = f"""# Startup Fail-Fast Report
- **Simulated Missing Artifact**: model.pkl
- **Exit Code**: {process.returncode}
- **Startup Log Output**:
```text
{process.stdout.strip()}
{process.stderr.strip()}
```
- **Status**: PASS
"""
        with open("reports/startup_failfast_report.md", "w") as f:
            f.write(report)
            
    finally:
        # Restore
        shutil.move(backup_path, model_path)
