import csv
from datetime import date
import smtplib
from email.mime.text import MIMEText
from parsers import dataDict, parseActorsAccess, ROOTURL

parserDate = dataDict["forDate"]

# MMDIP = Make More Dynamic If Possible


# daychars = ('mo','tu','we','th','fr','sa','su')
# rawDayNumber = date.today().isocalendar()[2] - 1
# day = daychars[rawDayNumber] # Variable 'day' is a two char string, ex. 'we'

# print(dataDict["date"],dataDict['time'])

def _recordData():

    with open("data.csv","r") as file:
        bottomLine = file.readlines()[-1]
        IDNumber = ""
        for char in bottomLine:    # Inch along the bottom line and pick up digits...
            if char.isdigit():
                IDNumber += char
            else: break    # ...until hitting a non-digit character.
        # This is the ID number of the previous runtime.

        dataDict["ID"] = int(IDNumber) + 1 # The ID of this runtime is the previous + 1

    with open("data.csv","a") as file:
        writer = csv.writer(file)
        writer.writerow(dataDict.values())

# You need to allow unidentified apps on an email to use SMTP, ergo uses dummy email for safety
USEREMAIL = "aaronlearns39@gmail.com"
def _sendEmail(text,date=parserDate,useremail=USEREMAIL):
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


def main(forDate=parserDate,sendEmail=True,recordData=True):

    # forDate works best as a string, because single-digit dates are found as 01, 02 etc.
    if (type(forDate) != str) or (type(sendEmail) != bool):
        raise Exception("\nUsage of main() parameters: fordate - string and sendEmail - bool\n")
    
    print('parsing website(s)...')
    AAmatchedDescs = parseActorsAccess(forDate)
    # matchedDescs_BS = parseBackstage
   
    print('writing to files...')
    with open("email.txt", "w") as f:
        for descList in AAmatchedDescs:
            f.write("<>" * 30)
            f.write("\n")
            url = ROOTURL + descList[-1] # Compose URL to put in email
            texts = descList[0:-1] # Everything else is the [name,description] lists
            for text in texts:
                name = text[0]
                description = text[1]
                f.write("[ {} ]\n{}\n\n".format(name,description))
            f.write("VIEW FULL CASTING CALL: {}\n".format(url)) # Put the URL under the roles.
    
    if recordData:
        print("recording data...")
        _recordData()
     
    if sendEmail:
        print("emailing to you...")
        with open("email.txt", "r") as f: text = f.read()
        _sendEmail(text,date=forDate)


    print('finished!')
    return 0
    

if __name__ == '__main__':
    main()
    # main(forDate="08",sendEmail=False)