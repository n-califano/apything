import os
import subprocess
import sys
import importlib.util

def is_installed(package_name):
    return importlib.util.find_spec(package_name) is not None


if not os.path.exists('test_env'):
    print("Virtual environment not found, creating it...")
    subprocess.check_call([sys.executable, '-m', 'venv', 'test_env'])

# Activate the virtual environment (Windows and Linux compatible)
activate_cmd = os.path.join('test_env', 'Scripts', 'activate') if os.name == 'nt' else os.path.join('test_env', 'bin', 'activate')
print("Activating virtual environment...")
subprocess.check_call([activate_cmd], shell=True)

#TODO: the package is not being installed in the test_env, but in the global env
#TODO: probably the activation of the previous command does not persist, fix it.
if not is_installed("apything"):
    print("Installing package in dev mode...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-e', '..'])
print("Package already installed in dev mode.")

print("Running pytest...")
subprocess.check_call([sys.executable, '-m', 'pytest'])
