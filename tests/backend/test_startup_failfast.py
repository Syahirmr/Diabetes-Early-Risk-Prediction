import pytest
from backend.startup.load_artifacts import load_all_artifacts

def test_startup_failfast(monkeypatch, tmp_path):
    # Simulate missing artifacts by changing the working directory to a tmp path
    monkeypatch.chdir(tmp_path)
    
    with pytest.raises(SystemExit) as exc_info:
        load_all_artifacts()
    
    assert exc_info.type == SystemExit
    assert exc_info.value.code == 1
