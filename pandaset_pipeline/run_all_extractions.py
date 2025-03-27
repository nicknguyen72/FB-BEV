import subprocess
import os
import sys

# Define scripts in order of execution
scripts = [
    "sensor_extraction.py",
    "calibrated_sensor_extraction.py",
    "ego_pose_extraction.py",
    "sample_extraction.py",
    "annotation_extraction.py",
    "sample_data_extraction.py",
    "scene_extraction.py"
]

# Base script path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

print("Running all extraction scripts in order:\n")
for script in scripts:
    script_path = os.path.join(SCRIPT_DIR, script)
    print(f"Running {script}...")
    try:
        result = subprocess.run([sys.executable, script_path], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error in {script}:\n{e.stderr}\n")
        break

print("All scripts completed.")
