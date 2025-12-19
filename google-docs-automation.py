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
    print(f"{f['name']} ({f['id']})")



