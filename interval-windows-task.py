import subprocess
from dotenv import load_dotenv
import os

#Get environment variables
load_dotenv()
WORKING_DIR = os.getenv("WORKING_DIR")
BATCH_PATH = os.getenv("BATCH_PATH")

SCRIPT_FILE_NAME = 'google-docs-automation.py'
LOG_FILE_NAME = 'scheduled-automation.log'

#Create batch file to execute the python script
batch_content = f"""@echo off
cd /d {WORKING_DIR}
echo Run at %date% %time% >> "{LOG_FILE_NAME}"
python "{SCRIPT_FILE_NAME}" >> "{LOG_FILE_NAME}" 2>&1
"""
with open(BATCH_PATH, "w") as f:
    f.write(batch_content)
print(f"Batch file created at: {BATCH_PATH}")

#Create scheduled task
subprocess.run(
    [
        "schtasks",
        "/create",
        "/tn", "AutoDownloadCVGoogleDocs",
        "/tr", f'cmd /c "{BATCH_PATH}"',
        "/sc", "minute",
        "/mo", "1",
        "/f"
    ],
    check=True
)

print("Scheduled task created: AutoDownloadCVGoogleDocs")
print(f"Logs will be written to: {LOG_FILE_NAME}")