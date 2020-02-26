from my_service import init_google_photos_api_service

import pandas as pd

# https://learndataanalysis.org/albums-resource-google-photos-api-and-python-part-2/

service = init_google_photos_api_service()

"""
list method
"""
response = service.albums().list(
    pageSize=50,
    excludeNonAppCreatedData=False
).execute()

lstAlbums = response.get('albums')
nextPageToken = response.get('nextPageToken')

while nextPageToken:
    response = service.albums.list(
        pageSize=50,
        excludeNonAppCreatedData=False,
        pageToken=nextPageToken
    )
    lstAlbums.extend(response.get('ablums'))
    nextPageToken = response.get('nextPageToken')

df_albums = pd.DataFrame(lstAlbums)


"""
get method
"""
# my_album_id = df_albums[df_albums['title'] == 'Jay\'s Photo']['id'][0]
my_album_id = df_albums[df_albums['title'] == '五姑婆（五位姑姑跟外婆）']['id'][0]
response = service.albums().get(albumId=my_album_id).execute()
print(response)


"""
create method
"""
request_body = {
    'album': {'title': 'My Family Photos'}
}
response_album_family_photos = service.albums().create(body=request_body).execute()


"""
addEnrichment (album description)
"""
request_body = {
    'newEnrichmentItem': {
        'textEnrichment': {
            'text': 'This is my family album'
        }
    },
    'albumPosition': {
        'position': 'LAST_IN_ALBUM'
    }
}

response = service.albums().addEnrichment(
    albumId=response_album_family_photos.get('id'),
    body=request_body
).execute()


"""
addEnrichment (album location aka map)
"""
request_body = {
    'newEnrichmentItem': {
        'locationEnrichment': {
            'location': {
                'locationName': 'San Francisco, IL',
                'latlng': {
                    'latitude': 41.875270,
                    'longitude': -87.18797
                }
            }
        }
    },
    'albumPosition': {
        'position': 'LAST_IN_ALBUM'
    }
}
response = service.albums().addEnrichment(
    albumId=response_album_family_photos.get('id'),
    body=request_body
).execute()


"""
addEnrichment (album map route)
"""
request_body = {
    'newEnrichmentItem': {
        'mapEnrichment': {
            'origin': {
                'locationName': 'Chicago, IL',
                'latlng': {
                    'latitude': 41.875270,
                    'longitude': -87.18797
                }
            },
            'destination': {
                'locationName': 'San Francisco, CA',
                'latlng': {
                    'latitude': 37.775981,
                    'longitude': -122.419343
                }
            }
        }
    },
    'albumPosition': {
        'position': 'FIRST_IN_ALBUM'
    }
}

response = service.albums().addEnrichment(
    albumId=response_album_family_photos.get('id'),
    body=request_body
).execute()


"""
Share and unshare methods
"""
request_body = {
    'sharedAlbumOptions': {
        'isCollaborative': True,
        'isCommentable': True
    }
}
response = service.albums().share(
    albumId=response_album_family_photos['id'],
    body=request_body
).execute()


service.albums().unshare(albumId=response_album_family_photos.get('id')).execute()

"""
batchAddMediaItems & batchRemoveMediaItems
"""
response = service.albums().list(
    pageSize=50,
    excludeNonAppCreatedData=False
).execute()

lstAlbums = response.get('albums')
nextPageToken = response.get('nextPageToken')

while nextPageToken:
    response = service.albums.list(
        pageSize=50,
        excludeNonAppCreatedData=False,
        pageToken=nextPageToken
    )
    lstAlbums.extend(response.get('ablums'))
    nextPageToken = response.get('nextPageToken')

df_albums = pd.DataFrame(lstAlbums)

album_id = df_albums['id'][0]  # 'My Family Photos'


response = service.mediaItems().list(pageSize=25).execute()

lst_medias = response.get('mediaItems')
nextPageToken = response.get('nextPageToken')

while nextPageToken:
    response = service.mediaItems().list(
        pageSize=25,
        pageToken=nextPageToken
    ).execute()
    lst_medias.extend(response.get('mediaItems'))
    nextPageToken = response.get('nextPageToken')

df_media_items = pd.DataFrame(lst_medias)
media_items_ids = df_media_items['id'][:3].to_list()

request_body = {
    'mediaItemIds': media_items_ids
}

response = service.albums().batchAddMediaItems(
    albumId=album_id,
    body=request_body
).execute()


response = service.albums().batchRemoveMediaItems(
    albumId=album_id,
    body=request_body
).execute()
