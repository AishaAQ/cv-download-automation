from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_PATH = os.getenv("BASE_PATH")

def download(file_id,file_name,file_type, service):

    if file_type == 'pdf':
        mime_type = 'application/pdf'
    else:
        mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    
    name_list = file_name.split('CV')
    folder_name = name_list[1].replace('_', ' ')[1:]
    if file_type == 'pdf': file_name = f"{file_name.split('CV')[0]}CV"
    
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

def main():

    SERVICE_ACCOUNT_FILE = 'service-account.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/drive.readonly'] 
    )

    service = build('drive', 'v3', credentials=credentials)

    results = service.files().list(
        pageSize=100, fields="files(id, name)"
    ).execute()

    files = results.get('files', [])

    for f in files:

        file_id = f['id']
        file_name = f['name']

        print(f"{f['name']} ({f['id']})")

        download(file_id,file_name,'pdf',service)
        download(file_id,file_name,'docx',service)

main()