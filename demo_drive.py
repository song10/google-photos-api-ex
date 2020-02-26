from my_service import init_google_drive_api_service
from googleapiclient.http import MediaFileUpload

import pandas as pd


def main():
    service = init_google_drive_api_service()

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    df_items = pd.DataFrame(items)
    print(df_items)

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for x in items:
            print(f"{x['name']} ({x['id']})")


"""
create folder
"""
file_metadata = {
    'name': 'Young Living',
    'mimeType': 'application/vnd.google-apps.folder'
}
responce = service.files().create(body=file_metadata,
                                  fields='id').execute()
print(f"Folder ID: {responce.get('id')}")


"""
insert a file
"""
folder_id = responce.get('id')
file_metadata = {
    'name': 'dogy.jpg',
    'parents': [folder_id]
}
media = MediaFileUpload('Images To Upload/dogy.jpg',
                        mimetype='image/jpeg',
                        resumable=True)
responce = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
print(f"File ID: {responce.get('id')}")

"""
move file between folders
"""
file_id = '1sTWaJ_j7PkjzaBWtNc3IzovK5hQf21FbOw9yLeeLPNQ'
folder_id = '0BwwA4oUTeiV1TGRPeTVjaWRDY1E'
# Retrieve the existing parents to remove
responce = service.files().get(fileId=file_id,
                               fields='parents').execute()
previous_parents = ",".join(responce.get('parents'))
# Move the file to the new folder
responce = service.files().update(fileId=file_id,
                                  addParents=folder_id,
                                  removeParents=previous_parents,
                                  fields='id, parents').execute()

if __name__ == '__main__':
    main()
