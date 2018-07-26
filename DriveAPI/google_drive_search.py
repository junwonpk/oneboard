from __future__ import print_function
import os
import io
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

service = None

def setup():
    global service
    SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
    store = file.Storage('token.json')
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        print (flow)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

def search(query, limit=10):
    filelist = []
    # Search through file names
    page_token = None
    while True:
        response = service.files().list(q="name contains '%s'" % query,
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)',
                                              pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            filelist.append((file.get('name'), file.get('id')))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    # Search through files
    page_token = None
    while True:
        response = service.files().list(q="fullText contains '%s'" % query,
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)',
                                              pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            filelist.append((file.get('name'), file.get('id')))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    for name, fileID in filelist[:limit]:
        print ('Found file: %s (%s)' % (name, fileID))

setup()
search('Microsoft')
