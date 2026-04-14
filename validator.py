import subprocess
import sys
import tempfile
import os


def validate_pytest(test_code: str) -> dict:
    with tempfile.NamedTemporaryFile(mode='w', suffix='_test.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", temp_path, "--tb=short"],
            capture_output=True,
            text=True
        )
    finally:
        os.unlink(temp_path)

    return {
        "passed": result.returncode == 0,
        "output": result.stdout,
        "errors": result.stdout + result.stderr
    }