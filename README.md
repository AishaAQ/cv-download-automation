# 🔄 CV Google Docs Download Automation Script

A Python script to automate downloading CVs from Google Docs on Google Drive as Word and PDF documents.

## ⚙️ Technologies

- `Python 3.14`
- `Google Drive API`
- `Google Cloud`
- `Windows Task Scheduler`

## ✨ Features

- Automates downloading specified Google Docs files if changes are detected from your local copies
- Schedules a task in `Windows Task Scheduler` that runs every 12 hours to detect changes and download the files

> **Note:** The `google-docs-automation.py` script is designed for CV files with a specific naming pattern but can be modified for other documents.
 
## 📍 Motivation

I needed an easier way to download my CV files from Google Docs, instead of manually downloading at every change.

## 🛠️ Project Setup

1. The Google Docs files need to follow one of the following naming patterns: `<your_name>_CV_<job_role>` or `<your_name>_CV`
2. Follow [this guide](https://developers.google.com/workspace/guides/create-project) to create a Google Cloud project.
3. Enable the Google Drive API in the created Google Cloud project following [this link](https://console.cloud.google.com/apis/enableflow;apiid=drive.googleapis.com).
4. Follow [this](https://docs.cloud.google.com/iam/docs/service-accounts-create) to create a service account in Google Cloud if you do not have one already.
   - The files that need to be downloaded will be granted access to this service account.
   - I recommend granting only Viewer role to this service account.
5. Create a key for your service account [here](https://console.cloud.google.com/iam-admin/serviceaccounts) and download the JSON file for the key.
  > ⚠️ **Warning:** Do not share the JSON file with anyone and store it securely.
6. Rename the JSON file to `service-account.json` and place it in the project directory.
7. Share the Google Docs that you need downloaded to the created service account with Viewer permissions.
8. Update the `.env.template` file with your values, then rename the file to `.env`.

## ▶️ Running the Project

1. Install the required dependencies
```bash
python -m pip install -r requirements.txt
```
2. Run the `google-docs-automation.py` script to download the Google Docs files
```bash
python google-docs-automation.py
```
3. Run the `` script to create a scheduled task that runs every 12 hours and downloads the modified Google Docs files
```bash
python schedule-download-task.py   
```
> **Note:** The logs of the latest run can be found in `scheduled-automation.log`.
