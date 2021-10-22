
from typing import Type
from parsers import dataDict, parseActorsAccess, ROOTURL
from helpers import _sendEmail, _recordData

parserDate = dataDict["forDate"]

# MMDIP = Make More Dynamic If Possible


# daychars = ('mo','tu','we','th','fr','sa','su')
# rawDayNumber = date.today().isocalendar()[2] - 1
# day = daychars[rawDayNumber] # Variable 'day' is a two char string, ex. 'we'

# print(dataDict["date"],dataDict['time'])

def main(forDate=parserDate,sendEmail=True,recordData=True):

    # forDate works best as a string, because single-digit dates are found as 01, 02 etc.
    if not isinstance(forDate, str):
        raise TypeError("main() forDate must be a string.")
    elif not isinstance(sendEmail, bool):
        raise TypeError("main() sendEmail must be a boolean.")
    elif not isinstance(recordData, bool):
        raise TypeError("main() recordData must be a boolean.")
    
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