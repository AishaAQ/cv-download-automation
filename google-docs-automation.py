from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import io
from datetime import datetime

def download(file_id,file_name,file_type):

    if file_type == 'pdf':
        mime_type = 'application/pdf'
    else:
        mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    
    name_list = file_name.split('CV')
    folder_name = name_list[1].replace('_', ' ')[1:]
    
    request = service.files().export_media(
        fileId=file_id,
        mimeType=mime_type
    )

    fh = io.FileIO('DownloadedDoc.' + file_type, 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}% complete")

    print("Download finished!")

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

    download(file_id,file_name,'pdf')
    download(file_id,file_name,'docx')