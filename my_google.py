from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import os
import pickle


def Create_Service(client_secret_file: str, api_name: str, api_version: str, scopes: list):
    # print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_NAME = api_name
    API_VERSION = api_version
    SCOPES = scopes

    cred = None

    pickle_file = f'token_{API_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    # The file {pickle_file} stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_NAME, API_VERSION, credentials=cred)
        print(API_NAME, 'service created successfully')
        return service
    except Exception as e:
        print(e)
    return None
