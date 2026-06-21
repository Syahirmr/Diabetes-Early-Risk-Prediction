import subprocess
import sys

commands = [
    ("Build Frontend", ["npm", "run", "build"]),
    ("Pytest", [".\\.venv\\Scripts\\pytest.exe"]),
    ("Ruff Check", [".\\.venv\\Scripts\\ruff.exe", "check", "."]),
    ("MyPy Backend", [".\\.venv\\Scripts\\mypy.exe", "backend"])
]

all_passed = True

for name, cmd in commands:
    print(f"=== Running {name} ===")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"{name} FAILED!")
        print(res.stdout)
        print(res.stderr)
        all_passed = False
    else:
        print(f"{name} PASSED.\n")

if not all_passed:
    sys.exit(1)
print("ALL PASSED.")
