from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

import pprint

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')                          # C:\Users\Username
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    # The get() function returns the credentials for the Storage object. If no
    # credentials were found, None is returned.
    credentials = store.get()
    # If no credentials are found or the credentials are invalid due to
    # expiration, new credentials need to be obtained from the authorization
    # server. The oauth2client.tools.run_flow() function attempts to open an
    # authorization server page in your default web browser. The server
    # asks the user to grant your application access to the user's data.
    # If the user grants access, the run_flow() function returns new credentials.
    # The new credentials are also stored in the supplied Storage object,
    # which updates the credentials.dat file.
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    
    credentials = get_credentials()
    
    # Create an httplib2.Http object to handle our HTTP requests, and authorize it
    # using the credentials.authorize() function.
    http = credentials.authorize(httplib2.Http())
    """
    The apiclient.discovery.build() function returns an instance of an API service
    object can be used to make API calls. The object is constructed with
    methods specific to the calendar API. The arguments provided are:
       name of the API ('calendar')
       version of the API you are using ('v3')
       authorized httplib2.Http() object that can be used for API calls
    """
    service = discovery.build('calendar', 'v3', http=http)  #('api-name','api-version',...)
    print(service)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    print(now)
    """
    The Calendar API's events().list method returns paginated results, so we
    have to execute the request in a paging loop. First, build the
    request object. The arguments provided are:
       primary calendar for user
    """
    eventsResult = service.events().list(
        calendarId='t9gtmeov9jkvdu9vr0p11dm72o@group.calendar.google.com', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    # response = request.execute()
    # response = request.stamps().list().execute()
    """
    The response is a Python object built from the JSON response sent
    by the API server. The JSON structure is specific to the API;
    for details, see the API's reference documentation. You can also
    simply print the JSON to see the structure:
    """
    pprint.pprint(eventsResult)
    print('\n')
    
    # Accessing the response like a dict object with an 'items' key
    # returns a list of item objects (events).
    events = eventsResult.get('items', [])
    pprint.pprint(events)
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))          #creates tuple
        print(type(start))
        
        # The event object is a dict object with a 'summary' key.
        print(start, event['summary'])


if __name__ == '__main__':
    main()
