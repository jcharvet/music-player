import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_package(package):
    """
    Check if a package is installed.

    Args:
        package (str): The name of the package to check.

    Returns:
        None
    """
    try:
        __import__(package)
    except ImportError:
        install(package)

def run_main():
    subprocess.check_call([sys.executable, "main.py"])

# List of required packages
required_packages = ["pygame", "tk", "mutagen", "pygame", "pyaudio", "numpy", "requests", "pillow"]

# Check and install each package
for package in required_packages:
    check_package(package)

# Run the main script
run_main()
