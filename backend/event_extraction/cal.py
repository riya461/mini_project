import datetime
import os.path
from event_extraction.cal_setup import get_calendar_service
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def run(summary, start_time, end_time, description = "Automated by ..."):
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("event_extraction/token.json"):
    creds = Credentials.from_authorized_user_file("event_extraction/token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "event_extraction/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("event_extraction/token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    # print("Getting the upcoming 10 events")
    # events_result = (
    #     service.events()
    #     .list(
    #         calendarId="primary",
    #         timeMin=now,
    #         maxResults=10,
    #         singleEvents=True,
    #         orderBy="startTime",
    #     )
    #     .execute()
    # )
    # events = events_result.get("items", [])

    # if not events:
    #   print("No upcoming events found.")
    #   return

    # # Prints the start and name of the next 10 events
    # for event in events:
    #   start = event["start"].get("dateTime", event["start"].get("date"))
    #   print(start, event["summary"])
    # calendar = {
    #   'summary': 'calendarSummary',
    #   'timeZone': 'America/Los_Angeles'
    # }

    

    # d = datetime.datetime.now().date() 
    # print(d)
    # tomorrow = datetime.datetime(d.year, d.month, d.day, 10)+datetime.timedelta(days=1)
    # start = tomorrow.isoformat()
    # end = (tomorrow + datetime.timedelta(hours=1)).isoformat()

    event_result = service.events().insert(calendarId='primary',
        body={
            "summary": summary,
            "description":description,
            "start": {"dateTime": start_time, "timeZone": 'Asia/Kolkata'},
            "end": {"dateTime": end_time, "timeZone": 'Asia/Kolkata'},
        }
    ).execute()

    print("created event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])


  except HttpError as error:
    print(f"An error occurred: {error}")

  



if __name__ == "__main__":
  run()