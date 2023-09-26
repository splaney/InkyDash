from __future__ import print_function
import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def upload_revision():
    """Update file.
    Returns : Id's of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('../gcal/token.pickle'):
        with open('../gcal/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../gcal/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../gcal/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Specify the ID of the file you want to update.
    file_id = '18tDjA9B-p_W7N_ks52ZLLu-4XvPI0X_W'

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        media = MediaFileUpload('../dash_update.jpeg',
                                mimetype='image/jpeg')
        # Use the files().update method to upload a revision.
        updated_file = service.files().update(
            fileId=file_id,
            media_body=media,
        ).execute()

        print(f'File ID: {updated_file.get("id")}')

    except HttpError as error:
        print(f'An error occurred: {error}')
        updated_file = None

    return updated_file.get('id') if updated_file else None


if __name__ == '__main__':
    upload_revision()

