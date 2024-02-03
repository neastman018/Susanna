import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

class Event:
  def __init__(self, minute, hour, day, month, year = 2023, summary = 'No Summary'):
    self.hour = hour
    self.minute = minute
    self.day = day
    self.month = month
    self.year = year
    self.summary = summary

  def toString(self):
    minute = self.minute
    if self.minute < 10:
      minute = f"0{self.minute}"
    hour = self.hour
    if self.hour < 10:
      hour = f"0{self.hour}"
    day = self.day
    if self.day < 10:
      day = f"0{self.day}"
    month = self.month
    if self.month < 10:
      month = f"0{self.month}"
    return f"{self.summary} - {hour}:{minute} {month}/{day}/{self.year}"




  """
  Gets the next ten events
  @return: the next 10 events in the calendar
  """

def get_events() -> list|Event:
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "creds.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    upcoming_events = []

    if not events:
      print("No upcoming events found.")
      return


    for i in range(0,10):
      # Prints the start and name of the next 10 events
      event = events[i]["start"].get('dateTime')
      event_minute = int(event[14] + event[15])
      event_hour = int(event[11] + event[12])
      event_day = int(event[8] + event[9])
      event_month = int(event[5] + event[6])
      event_year = int(event[0] + event[1] + event[2] + event[3])
      event_summary = events[i]["summary"]

      new_event = Event(event_minute, event_hour, event_day, event_month, event_year, event_summary)

      upcoming_events.append(new_event)

    return upcoming_events
    
  except HttpError as error:
    print(f"An error occurred: {error}")

"""
Checks the next 10 events for the next alarm
"""

def get_next_alarm():
  upcoming_events = get_events()
  now = datetime.datetime.now()
  for event in upcoming_events:
    # check if the event in an alarm
    if event.summary == 'Alarm':
      # check if alarm is in the next 24 hours
      # if today
      if event.year == now.year and event.month == now.month and event.day == now.day:
        return event
      # if tomorrow and not the start of a month
      elif event.day == now.day+1 and event.month == now.month and event.hour <= now.hour:
        return event
      # if tomorrow and it is the 31st of a mont
      elif now.day == 31 and event.day == 1 and event.month == now.month+1 and event.hour <= now.hour:
        return event
      # if tomorrow and it is a 30 day month
      elif now.month == 9 or now.month == 4 or now.month == 6 or now.month == 9:
        if now.day == 30 and event.day == 1 and event.month == now.month+1 and event.hour <= now.hour:
          return event
      # if tomorrow is 3/1
      if now.month == 2 and now.day == 28 and event.day == 1 and event.month == now.month+1 and event.hour <= now.hour:
        return event
      # if it is new years
      if now.month == 12 and now.day == 31 and event.day == 1 and event.month == 1 and event.year == now.year+1 and event.hour <= now.hour:
        return event
      

      


      



if __name__ == "__main__":
  if get_next_alarm() == None:
    print("No Alarms Upcoming")
  else:
    print(get_next_alarm().toString())