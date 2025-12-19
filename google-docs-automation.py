from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import io
from datetime import datetime

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

    request = service.files().get_media(fileId=file_id)

    print(f"{f['name']} ({f['id']})")

    fh = io.FileIO('DownloadedDoc.docx', 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}% complete")

    print("Download finished!")

