#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from __future__ import print_function
import httplib2
import os
import apiclient
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/admin-directory_v1-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Directory API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'admin-directory_v1-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def print_users(service):
    results = service.users().list(customer='my_customer', maxResults=10,
        orderBy='email').execute()
    users = results.get('users', [])
    
    if not users:
        print('No users in the domain.')
    else:
        print('Users:')
        for user in users:
            print('{0} ({1})'.format(user['primaryEmail'],
                user['name']['fullName'].encode('utf8') ))
                #user['name']['fullName']))

def update_emails(service):
    user = service.users().get(userKey='alexander.kiyanov@deploy.ltd',
                                 projection='full').execute()
    newEmails = []
    for email in user['emails']:
        #print(email)
        if 'primary' in email:
            newEmails.append({u'address': email[u'address'], u'primary': True})
            #newEmails.append({u'address': email[u'address']})
        elif 'customType' in email:
            continue
        else:
            newEmails.append({u'address': email[u'address']})
    #newEmails.append({u'address': u'alexander.kiyanov@embria-group.com', u'primary': True})
    print (user['emails'])
    #for i in newEmails:
    #  print(i)
    newEmails.append({u'address': u'testak@deploy.ltd'})
    user['emails'] = newEmails
    result = service.users().update(userKey='alexander.kiyanov@deploy.ltd',
                                    body=user).execute()
    print(result) 


def get_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('admin', 'directory_v1', http=http)
    return service



def main():
    """Shows basic usage of the Google Admin SDK Directory API.

    Creates a Google Admin SDK API service object and outputs a list of first
    10 users in the domain.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('admin', 'directory_v1', http=http)

    #update_emails(service)
    print(service.users().list(customer='my_customer').execute())
    #print('Getting the first 10 users in the domain')


if __name__ == '__main__':
    main()
