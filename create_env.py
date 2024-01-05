# Create a virtual environment. Only needed once or for development.
import os
import platform
import subprocess
import sys

venv_name = "instabot"

def create_virtualenv(venv_name):
    python_executable = sys.executable
    venv_command = "python -m venv" if platform.system() == "Windows" else "python3 -m venv"

    # Create a virtual environment
    subprocess.run(f"{venv_command} {venv_name}", shell=True, check=True)

    # Activate the virtual environment
    activate_command = (
        os.path.join(venv_name, "Scripts", "activate.bat")
        if platform.system() == "Windows"
        else f"source {venv_name}/bin/activate"
    )
    subprocess.run(activate_command, shell=True, check=True)

    # Upgrade pip and install any necessary packages
    ## ISSUE: insufficient permissions on Windows. Added '--user'
    subprocess.run("python -m pip install --upgrade pip --user", shell=True, check=True)

    # Get the full path to the pip executable in the virtual environment
    pip_path = os.path.join(venv_name, "Scripts", "pip.exe") if platform.system() == "Windows" else f"{venv_name}/bin/pip"

    # Install necessary packages using the full path to pip
    subprocess.run(f"{pip_path} install -r requirements.txt", shell=True, check=True)

if __name__ == "__main__":
    create_virtualenv(venv_name)