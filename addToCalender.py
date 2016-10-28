
import httplib2
import os


from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import copy
import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'googleCredentials/client_secret.json'
APPLICATION_NAME = 'SotonUniTimetable'


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
                                   'googleAuthSotonTimetableAdder.json')

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


def formatClassesToJson(timeTableClasses):

    events_list = []
    for sotonClass in timeTableClasses:
        events_list.append(buildEventJson(sotonClass))
    return events_list


def buildEventJson(classObject):

    event = {
        'summary': classObject.name,
        'location': classObject.location,
        'start': {
            'dateTime': classObject.start_time.isoformat('T'),
            'timeZone': 'Europe/London',
        },
        'end': {
            'dateTime': classObject.end_time.isoformat('T'),
            'timeZone': 'Europe/London',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 15},
            ],
        },
    }
    return event

def removeDuplicates(service, events_to_add):

    def try_parsing_date(text):
        for fmt in ('%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:', '%Y-%m-%dT%H:%M'):
            try:
                return datetime.datetime.strptime(text, fmt)
            except ValueError:
                pass
        raise ValueError('no valid date format found')

    minTime = (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat('T')[:-7] + "Z"
    eventsResult = service.events().list(
        calendarId='primary', timeMin=minTime, maxResults=100, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    current_event_list = []
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        current_event_list.append([start, event['summary']])

    event_to_add_updated_list = copy.deepcopy(events_to_add)
    for event_to_add in events_to_add:
        for current_event in current_event_list:
            if event_to_add["summary"] in (current_event[1]):
                event_to_add_start_date = try_parsing_date(event_to_add["start"]["dateTime"])
                current_event_start_date = try_parsing_date(current_event[0][:-6])
                if event_to_add_start_date == current_event_start_date:
                    if event_to_add in event_to_add_updated_list:
                        event_to_add_updated_list.remove(event_to_add)
    return event_to_add_updated_list




def addTocalendar(timeTableClasses):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    events_to_add = formatClassesToJson(timeTableClasses)
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    events_to_add_minus_duplicates = removeDuplicates(service, events_to_add)

    for event in events_to_add_minus_duplicates:
        eventAdded = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (eventAdded.get('htmlLink')))



