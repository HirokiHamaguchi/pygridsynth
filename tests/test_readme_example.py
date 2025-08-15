"""
Test for examples/mpf.py and README.md example consistency
"""

import os
import subprocess
import sys
from typing import Tuple

import mpmath
import pytest

from pygridsynth.gridsynth import gridsynth_gates

# Path to the example file
EXAMPLE_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "examples", "mpf.py")

# Constants for example parameters (extracted from examples/mpf.py)
EXAMPLE_DPS = 128
EXAMPLE_THETA = "0.5"
EXAMPLE_EPSILON = "1e-10"


def _read_example_file_content() -> str:
    """Read the content of the examples/mpf.py file"""
    with open(EXAMPLE_FILE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def _extract_readme_example_code() -> str:
    readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()
    readme_lines = readme_content.split("\n")

    # Find the specific code block
    start_line = None
    end_line = None

    for i, line in enumerate(readme_lines):
        if line.strip() == "import mpmath":
            start_line = i
        elif start_line is not None and line.strip() == "print(gates)":
            end_line = i
            break

    if start_line is None or end_line is None:
        raise ValueError("Could not find README example code block")

    return "\n".join(readme_lines[start_line : end_line + 1]) + "\n"


def _run_standalone_file(file_path: str) -> Tuple[int, str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.join(os.path.dirname(__file__), "..")

    result = subprocess.run(
        [sys.executable, file_path],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(__file__),
        env=env,
    )

    return result.returncode, result.stdout, result.stderr


def _setup_example_parameters():
    mpmath.mp.dps = EXAMPLE_DPS
    theta = mpmath.mpmathify(EXAMPLE_THETA)
    epsilon = mpmath.mpmathify(EXAMPLE_EPSILON)
    return gridsynth_gates(theta=theta, epsilon=epsilon)


def test_example_execution():
    gates = _setup_example_parameters()
    assert gates is not None
    print(f"✓ Example executed successfully, result: {gates}")


def test_readme_example_content_matches():
    readme_example = _extract_readme_example_code()
    example_file_content = _read_example_file_content()
    assert readme_example == example_file_content
    print("✓ README example content matches examples/mpf.py")


def test_example_file_execution():
    # Test direct execution of examples/mpf.py
    returncode, stdout, stderr = _run_standalone_file(EXAMPLE_FILE_PATH)
    assert returncode == 0, f"Example file execution failed with error: {stderr}"
    assert stdout.strip(), "Example file should produce output"

    print(f"✓ examples/mpf.py executed successfully: {EXAMPLE_FILE_PATH}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
    print("All example tests passed!")
