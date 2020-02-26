from my_google import Create_Service

# https://learndataanalysis.org/getting-started-with-google-photos-api-and-python-part-1/

CLIENT_SECRET_FILE = 'client_secret_GoogleAPIExercise_PhotoDesktopApp.json'


def init_google_photos_api_service():
    API_NAME = 'photoslibrary'
    API_VERSION = 'v1'
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/photoslibrary',
              'https://www.googleapis.com/auth/photoslibrary.sharing']
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    return service


def init_google_drive_api_service():
    API_NAME = 'drive'
    API_VERSION = 'v3'
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/drive.file',
              'https://www.googleapis.com/auth/drive.metadata.readonly']
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    return service

def init_google_sheet_api_service():
    API_NAME = 'sheets'
    API_VERSION = 'v4'
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/drive.file',
              'https://www.googleapis.com/auth/spreadsheets']
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    return service
