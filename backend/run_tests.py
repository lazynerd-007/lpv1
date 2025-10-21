#!/usr/bin/env python3
"""
Test runner for LemonNPie Backend API
"""
import subprocess
import sys
import os


def run_tests():
    """Run the test suite"""
    # Set environment variables for testing
    os.environ["SECRET_KEY"] = "test-secret-key-for-testing"
    os.environ["DEBUG"] = "true"
    
    # Run pytest with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--cov=app",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "--tb=short"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ All tests passed!")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return e.returncode


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)