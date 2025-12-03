# Umbrella reminder program
# project picked from chapter 16 of Automate the Boring Stuff with Python

# THINGS YOU MAY WANT TO CHANGE AFTER YOU HAVE THIS PROGRAM:
# line 22: the URL should be the 7-day forecast page for your own location
# line 68: my_number should be the phone number at which you'd like to receive texts

import re

# THE BELOW MODULES DO NOT COME WITH PYTHON; YOU NEED TO INSTALL THEM
# try typing these into the terminal/command line:
# pip install requests
# pip install beautifulsoup4
# pip install twilio
import requests, bs4
from twilio.rest import Client
# Requests: downloads stuff from Internet
# Beautiful Soup: parses HTML
# Twilio: text message capability

# get page; CURRENTLY SET FOR WASHINGTON, DC
page = requests.get("https://forecast.weather.gov/MapClick.php?textField1=38.89&textField2=-77.03")
page.raise_for_status()
page_soup = bs4.BeautifulSoup(page.text, "html.parser")

# look for rain keywords in certain places (e.g. "chance of precipitation")

# it looks like we want the top two rows (daytime/nighttime) of the table under "Detailed Forecast")
# select element with class "row" inside element with id "detailed-forecast-body"
forecast_rows = page_soup.select("#detailed-forecast-body .row")
# this makes forecastRows a list of HTML stuff, one "row" from the HTML page per Python list item

# we only care about the first two rows
forecast_daytime = forecast_rows[0]
forecast_nighttime = forecast_rows[1]

# keyword: "Chance of precipitation is xx%." only shows if chance if 20% or higher

# look for associated % and record daytime/nighttime %s
rain_daytime = False
rain_day_chance = 0
rain_nighttime = False
rain_night_chance = 0
keyphrase = "Chance of precipitation is (\d\d)"
match = re.search(keyphrase, str(forecast_daytime))
if match:
    rain_daytime = True
    rain_day_chance = match.group(1)
match = re.search(keyphrase, str(forecast_nighttime))
if match:
    rain_nighttime = True
    rain_night_chance = match.group(1)

# if chance of rain:
#   • make a string that has an umbrella reminder, approximate time(s) of (potential) rain, and the associated %s
#   • send text to my number
if rain_daytime or rain_nighttime:
    reminder = "Pack an umbrella! Chances of rain: "
    reminder += rain_day_chance + "% during the day, "
    reminder += rain_night_chance + "% during the night."
    # for the heck of it:
    print(reminder)
    # prepare to send the text
    auth_sid = "AC3b0c64a63653d9c46ac5277b310d2d01"
    auth_token = "0b3e625cc1a0a644164eae8db340a9d6"
    twilio_client = Client(auth_sid, auth_token)
    from_number = "+15713653132"
    my_number = "" # FILL IN YOUR NUMBER including country code (+1 at the start if USA)
    # time to send the text
    twilio_client.messages.create(body=reminder, from_=from_number, to=my_number)