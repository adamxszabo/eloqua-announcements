import requests, dateutil.parser
from bs4 import BeautifulSoup
from datetime import datetime

#send email function
def sendEmail(title):
    requests.post(
    		"https://api.eu.mailgun.net/v3/YOUR-DOMAIN/messages",
    		auth=("api", "YOUR-API-KEY"),
    		data={"from": "YOUR-NAME <YOUR-EMAIL-ADDRESS>",
    			"to": ["YOUR-EMAIL-ADDRESS"],
    			"subject": title,
    			"text": "There is a new announcement on the Eloqua website: https://community.oracle.com/topliners/categories/eloqua-system-status"})

#get source code
request = requests.get("https://community.oracle.com/topliners/categories/eloqua-system-status", headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"})

#get last update date and title
sourceCode = BeautifulSoup(request.content)
timeElement = sourceCode.time.string
titleElement = sourceCode.find_all("div", {"class": "Title"})
title = titleElement[0].a.string
lastUpdate = dateutil.parser.parse(timeElement)

#get current time and date
now = datetime.now()

#if dates match and there is max one hour difference, then send email
difference = now - lastUpdate

if difference.days == 0 and difference.seconds <= 3600:
    sendEmail(title)
else:
    print("No new Eloqua updates")
