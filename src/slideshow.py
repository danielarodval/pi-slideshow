from src.common_imports import *
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def loop(root):
    # loop through images in directory
    img_dir = 'images'
    img_files = os.listdir(img_dir)
    img_files = [f for f in img_files if f.endswith('.jpg') or f.endswith('.png')]

    # load images
    img_arr = []
    for img_file in img_files:
        img_path = os.path.join(img_dir, img_file)
        img = Image.open(img_path)
        img = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        img_arr.append(img)

    panel = tk.Label(root, image=img)
    panel.pack(side="top", fill="both", expand="yes")
    
    return img_arr, img_files, panel

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

def find_folder(service, name):
    query = f"name = '{name}' and mimeType = 'application/vnd.google-apps.folder'"
    results = service.files().list(q=query, spaces='drive', fields="files(id, name)").execute()
    folders = results.get('files', [])
    return folders[0] if folders else None


def gdrive():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        # find the 'pi-slideshow' folder
        pi_slideshow_folder = find_folder(service, 'pi-slideshow')
        if not pi_slideshow_folder:
            print("No 'pi-slideshow' folder found.")
            return
        
        # Modify query to search within the 'pi-slideshow' folder and its subfolders for specific file types
        query = f"('{pi_slideshow_folder['id']}' in parents) and (mimeType='image/jpeg' or mimeType='image/png or mimeType='image/jpg')"
        results = (
            service.files()
            .list(q=query, pageSize=10, fields="files(id, name, parents)")
            .execute()
        )
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(f"{item['name']} ({item['id']})")

        return items
    except HttpError as err:
        print(f"An error occurred: {err}")