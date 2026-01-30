from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from dotenv import load_dotenv
from datetime import datetime, timezone
from pathlib import Path
import os
import json

load_dotenv()

BASE_PATH = os.getenv("BASE_PATH")

keywords = ['CV', 'Cover_Letter']

def download(file_id,file_name,file_type, service):

    if file_type == 'pdf':
        mime_type = 'application/pdf'
    else:
        mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    
    for k in keywords:
        if k in file_name:
            keyword = k
            break

    name_list = file_name.split(keyword)
    folder_name = name_list[1].replace('_', ' ')[1:]
    if file_type == 'pdf': file_name = f"{file_name.split(keyword)[0]}{keyword}"
    
    request = service.files().export_media(
        fileId=file_id,
        mimeType=mime_type
    )

    path = Path(f'{BASE_PATH}/{folder_name}')
    path.mkdir(parents=True, exist_ok=True)

    fh = open(path / f"{file_name}.{file_type}", "wb")
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}% complete")

    print("Download finished!")

def check_modified(modified_time_stamp,local_last_modified_timestamp):
        
    modified_time = datetime.strptime(modified_time_stamp[:-1], "%Y-%m-%dT%H:%M:%S.%f")
    modified_time = modified_time.replace(tzinfo=timezone.utc)
    if local_last_modified_timestamp:
        local_last_modified_time = datetime.strptime(local_last_modified_timestamp[:-1], "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=timezone.utc)
    else:
        local_last_modified_time = None
    
    return local_last_modified_time is None or modified_time > local_last_modified_time

def main():

    SERVICE_ACCOUNT_FILE = 'service-account.json'
    LAST_MODIFIED_FILE = f'{BASE_PATH}/last_modified.json'

    try:
        with open(LAST_MODIFIED_FILE, "r") as f:
            last_modified = json.load(f)
    except FileNotFoundError:
        last_modified = {}

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/drive.readonly'] 
    )

    service = build('drive', 'v3', credentials=credentials)

    results = service.files().list(
        pageSize=100, fields="files(id, name, modifiedTime)"
    ).execute()

    files = results.get('files', [])

    for f in files:

        file_id = f['id']
        file_name = f['name']
        modified_time_stamp = f['modifiedTime']

        local_last_modified_timestamp = last_modified.get(file_id)

        if check_modified(modified_time_stamp,local_last_modified_timestamp):
            
            print(f"File changed: {file_name}, downloading...")
            download(file_id,file_name,'pdf',service)
            download(file_id,file_name,'docx',service)
        
            last_modified[file_id] = modified_time_stamp
        
        else:
            print(f"No change: {file_name}, skipping download.")
    
    with open(LAST_MODIFIED_FILE, "w") as f:
        json.dump(last_modified, f, indent=2)

    print("Done checking all files.")

try:
    main()
except Exception as e:
    print(e)
    input('enter to close')

