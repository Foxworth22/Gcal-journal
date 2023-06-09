from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def new_event(service, summary, location, description, start_dateTime, start_timeZone, end_dateTime, end_timeZone):  
# to skip a param simply input '' for it
# all calls to new_event() must pass service as first parameter to maintain access
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': '2015-05-28T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2015-05-28T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'recurrence': [  # TODO: learn and parametrize
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
        'attendees': [
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
        ],
        'reminders': {
            'useDefault': True,
            'overrides': [
            # {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print ('Event created: %s' % (event.get('htmlLink')))

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('\tGetting the upcoming 10 events...')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
        print("\n", end="")  # same as print()

        # Print list of calendars -> Example from https://developers.google.com/calendar/api/v3/reference/calendarList/list#examples
        # Documentation for calendar_list_entry[] https://developers.google.com/calendar/api/v3/reference/calendarList#resource
        page_token = None
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            all_calendars = calendar_list['items']  # self-defined modulation for future re-use
            for calendar_list_entry in all_calendars:
                string = calendar_list_entry['summary']
                print ("%30s" % string[0:30], end=" ")
                print(":", end=" ")
                print (calendar_list_entry['id'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        print ("\n\tdone.")

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()