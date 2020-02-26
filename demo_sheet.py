from my_service import init_google_sheet_api_service, init_google_drive_api_service
from apiclient import errors

import pandas as pd

SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'


def main():
    service = init_google_sheet_api_service()
    drive_service = init_google_drive_api_service()

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(f'{row[0]}, {row[4]}')


"""
search file
"""
file_name = 'dogy'
response = drive_service.files().list(q=f"name contains '{file_name}'",
                                      spaces='drive',
                                      fields='files(id, name, parents)').execute()
file_ = response.get('files', [None])[0]
print(file_)

"""
list folders
"""
items = []
page_token = None
while True:
    response = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=page_token).execute()
    items.extend(response.get('files', []))
    page_token = response.get('nextPageToken', None)
    if page_token is None:
        break

pd_items = pd.DataFrame(items)
print(pd_items)


"""
search folder
"""
folder_name = 'Young Living'
response = drive_service.files().list(q=f"name = '{folder_name}' and mimeType='application/vnd.google-apps.folder'",
                                      spaces='drive',
                                      fields='files(id, name, parents)').execute()
folder = response.get('files', [None])[0]
print(folder)

"""
create sheet
"""
spreadsheet_body = {
    'properties': {
        'title': '產品目錄'
    }
}
spreadsheet = service.spreadsheets().create(body=spreadsheet_body,
                                            fields='spreadsheetId').execute()
print(spreadsheet)


"""
move file between folders
"""
file_id = spreadsheet['spreadsheetId']
folder_id = folder['id']
# Retrieve the existing parents to remove
responce = drive_service.files().get(fileId=file_id,
                                     fields='parents, name').execute()
previous_parents = ",".join(responce.get('parents'))
# Move the file to the new folder
responce = drive_service.files().update(fileId=file_id,
                                        addParents=folder_id,
                                        removeParents=previous_parents,
                                        fields='id, parents').execute()

"""
delete file
"""
file_name = '產品目錄'
response = drive_service.files().list(q=f"name contains '{file_name}'",
                                      spaces='drive',
                                      fields='files(id, name, parents)').execute()
file_id = response['files'][1]['id']
try:
    drive_service.files().delete(fileId=file_id).execute()
except errors.HttpError as error:
    print(f'An error occurred: {error}')


"""
get/set cells
"""
spreadsheet_id = response['files'][0]['id']
cell_range = 'A2:E3'
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=spreadsheet_id,
                            range=cell_range).execute()
values = result.get('values', [])

##
values = [
    [
        11, 22, 33, 44
    ],
    # Additional rows ...
    # [
    #     55, 66
    # ],
    [
        666, 777, 888, 999
    ],
]
body = {
    'values': values
}
result = sheet.values().update(
    spreadsheetId=spreadsheet_id,
    range=cell_range,
    valueInputOption="USER_ENTERED",
    body=body).execute()
print(result)


if __name__ == '__main__':
    main()
