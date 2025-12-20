import subprocess
from dotenv import load_dotenv
import os

load_dotenv()

SCRIPT_PATH = os.getenv("SCRIPT_PATH")

subprocess.run(
    [
        "schtasks",
        "/create",
        "/tn", "AutoDownloadCVGoogleDocs",
        "/tr", f"python3 {SCRIPT_PATH}",
        "/sc", "hourly",
        "/mo", "12",
        "/f"
    ],
    check=True
)
