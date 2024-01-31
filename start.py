import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_package(package):
    try:
        __import__(package)
    except ImportError:
        install(package)

def run_main():
    subprocess.check_call([sys.executable, "main.py"])

# List of required packages
required_packages = ["pygame", "tk"]

# Check and install each package
for package in required_packages:
    check_package(package)

# Run the main script
run_main()
