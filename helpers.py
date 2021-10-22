
from bs4 import BeautifulSoup

import csv
from datetime import date
import smtplib
from email.mime.text import MIMEText

from parsers import dataDict

def cleanString(input):
    input = input.replace('®', 'reg')
    input = input.replace('<br/>', ' ')
    input = input.replace('\n', ' ')
    input = input.replace('amp;','')
    return str(input)

def countNestedListElements(inList):
    elementCount = 0
    for element in inList:
        if type(element) == list:
            # print("calling")
            elementCount += countNestedListElements(element)
        else:
            elementCount += 1
        # print("elementCount: " + elementCount)
    return elementCount
# print(countNestedListElements([1,3,2,[4,4,8],3,[4,542,7],0]))

def getPageTitle(sessionGotUrl):
    soup = BeautifulSoup(sessionGotUrl.text, 'html.parser')
    title = soup.title
    return str(title)

def _recordData():

    DataFileName = "runtimeData.csv"

    with open(DataFileName,"r") as file:
        bottomLine = file.readlines()[-1]
        IDNumber = ""
        for char in bottomLine:    # Inch along the bottom line and pick up digits...
            if char.isdigit():
                IDNumber += char
            else: break    # ...until hitting a non-digit character.
        # This is the ID number of the previous runtime.

        dataDict["ID"] = int(IDNumber) + 1 # The ID of this runtime is the previous + 1

    with open(DataFileName,"a") as file:
        writer = csv.writer(file)
        writer.writerow(dataDict.values())

# You need to allow unidentified apps on an email to use SMTP, ergo uses dummy email for safety
USEREMAIL = "aaronlearns39@gmail.com"
parserDate = dataDict["forDate"]
def _sendEmail(text,date=parserDate,useremail=USEREMAIL):
        if not isinstance(text,str):
            raise TypeError("_sendEmail text must be a string")
        elif not isinstance(date,str):
            raise TypeError("_sendEmail date must be a string.")
        elif not isinstance(useremail,str):
            raise TypeError("_sendEmail useremail must be a string.")

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        serverEmail = 'jclay38craycray@gmail.com'
        serverPassword = 's3c^h&*2@jl'
        server.login(serverEmail,serverPassword)

        months = ("January","February","March","April","May","June",
        "July","August","September","October","November","December")

        suffixes = ("st","nd","rd","th")
        suffixNum = 3

        dateString = dataDict["date"][-5:]
        month = dateString[:2]
        dateText = date
        month = months[int(month) - 1]
        
        if int(dateText[1]) in [1,2,3] and int(dateText[0]) != 1:
            suffixNum = int(dateText[1]) - 1 # If there's a 1, write '1st', 2 write '2nd' etc.
        
        if int(dateText) < 10:
            dateText = dateText[1] # Prevent saying "october 08th" for single digit dates.

        message = MIMEText('Your casting calls for today have come in! Here are the roles you\'ve matched:\n\n{}'.format(text))
        message['Subject'] = "Your Casting calls for {} {}{}.".format(month,date,suffixes[suffixNum])


        server.sendmail(serverEmail, useremail, message.as_string())
        server.quit()



# Determines whether a call was posted on the current date
# Takes a get requested page as an argument.
