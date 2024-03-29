import requests
from requests import sessions
import urllib.parse
from login import AAusername, AApassword

import re

from bs4 import BeautifulSoup

from helpers import cleanString, countNestedListElements, getPageTitle, dataDict
from settings import ROOTURL, USERVARS, REGIONNUM

# A lot of the runtime data is gathered in the parsing process, which is why so much boiler-plate
# information is here and not in the main.
def AACallIsToday(callPage, globalDay):
    # print("Checking whether a call was today...")
    soup = BeautifulSoup(callPage.text, 'html.parser')
    # print(soup.title)

    callInfo = str(soup.td)
    # print("\ncallInfo:\n","<>"*30,"\n",callInfo + "\n","<>"*30,"\n")
    index = callInfo.find('>') + 1
    char = callInfo[index:index + 2]
    char = char.lower()

    # print("character is: " + char)

    return char == globalDay

"""
The inList is matchedDescs, which comes a specific struture can be found in parseActorsAccess.

The function itself returns data about the number of roles/calls matched for the data file.
"""
from reader import descUserMatched

def readAACall(href,inList,userSession):
    # Type checking
    types = (str,list,sessions.Session)
    args = (href,inList,userSession)
    for i,typ in enumerate(types):
        if not isinstance(args[i],typ):
            raise TypeError(f"readAACall {args[i]} must be a {typ}")

    # Gets the URL, then checks for session timeout and if so retries.
    desiredUrl = ROOTURL + href
    session = userSession
    s = session.get(desiredUrl)
    title = getPageTitle(s)
    # print(title)
    if 'login' in title:
        while True:
            print('Redirected to Login Page, retrying...')
            s = session.get(desiredUrl)
            if 'login' not in title:
                break
    soup = BeautifulSoup(s.text, 'html.parser')
    # print(soup.title)
    # print("<>" * 30)

    # Finds the raw text of the casting call and converts it to a string. It's a continuous string of all the
    # characters' names, each followed by a description of them ([ NAME ] \n description \n [ NAME ] \n description...)
    rawCall = ""
    for td in soup.select('td'):
        # print(td.attrs)    
        if not td.attrs:
            rawCall = td
    # print(rawCall)
    rawCall = str(rawCall)
    descs = []
    names = []
    # break

    # Makes a soup object out of this text to be parsed and read.
    rawCallSoup = BeautifulSoup(rawCall, 'html.parser')
    # print(rawCallSoup)
    # print(rawCallSoup.text)

    # This gets the name of the character being described, so if it's a match it can be sent in the email.
    nameRegex = re.compile("\[\s?(.+?)\s?\]")
    text = str(rawCallSoup.text)

    # This is the actual getting of the name from the matched call.
    nameIter = re.finditer(nameRegex,text)
    nameMatchObjects = []
    for iterObject in nameIter:
        nameMatchObjects.append(iterObject)        
    for i,matchObject in enumerate(nameMatchObjects):
        # print(matchObject)
        names.append(matchObject.group(1))
        desc = ""
        if i == len(nameMatchObjects)-1:
            desc = text[matchObject.end():]
        else:
            endIndex = text.find("[",matchObject.end())
            # print(endIndex)
            desc = text[matchObject.end():endIndex]
        descs.append(desc)

    # print(descs)
    # print("<>" * 30)
    # print(names)
    # print("<>" * 30)


    # Checks to make sure the name/description formatting went correctly.
    if len(names) != len(descs):
        big = 'descriptions'
        small = 'names'
        if len(names) > len(descs):
            big = 'names'
            small = 'descriptions'
        raise ValueError("Found more {} than {}.".format(big,small))


    # Variables for data appendage to csv
    matchedCalls = len(inList)
    currentRoles = int((countNestedListElements(inList) - matchedCalls) / 2)
 
    # In a casting call, only some of the roles may be matched, the ones that do get appended to matchedDescsOnCall.
    matchedDescsOnCall = []
    for i,d in enumerate(descs):
        # print("description: ",d,"\nname: ",names[i])
        descName = names[i]
        readableDesc = descName + " " + d # Each description includes the name
        readableDesc = cleanString(readableDesc)
        if d == "":
            d = "No description found."
        # print("description on-call number: ", i+1)
        # print("text:\n", d)
        if descUserMatched(USERVARS,readableDesc):
            currentRoles += 1
            # print("currentRoles :", currentRoles)
            matchedDescsOnCall.append([descName,d])
            print("role matched for user ({})".format(currentRoles))
    if len(matchedDescsOnCall) > 0:
        matchedCalls += 1
        # print("call matched for user ({})".format(len(inList)+1))
        matchedDescsOnCall.append(href)
        inList.append(matchedDescsOnCall)
    # print("finished reading a call")

    newRolesAmount = currentRoles
    newMatchedCallsAmount = matchedCalls
    # print(descs)
    # print("<>" * 30)
    # print(names)
    # print("<>" * 30)
    
    # These get added to runtime.csv
    return (newRolesAmount,newMatchedCallsAmount)
# print(readAACall("/projects/?view=breakdowns&breakdown=718453&region=32",[],requests.Session()))
# print(readAACall('/projects/index.cfm?view=breakdowns&breakdown=720452&region=32',[],requests.Session()))
# print("final:\n",readAACall('/projects/?view=breakdowns&breakdown=720768&region=32',[],requests.Session()))

# Finds a casting call withing the Actor's Access site architecture
def parseActorsAccess(currentDate):
    
    # Type checking
    if not isinstance(currentDate,str):
        raise TypeError("parseActorsAccess currentDate must be a string.")

    # For runtime.csv
    dataDict["forDate"] = currentDate

    # Logging in
    session = requests.Session()
    print("logging in...")
    # Log in and navigate to the calls page
    login = {'username' : AAusername, 'password' : AApassword}
    s = session.post('https://actorsaccess.com/index.cfm?login&loginSecure', data = login)
    s = session.get('https://actorsaccess.com/projects/index.cfm?region={}'.format(urllib.parse.quote_plus(REGIONNUM)))

    # Getting the casting calls as they appear on the homepage.
    soup = BeautifulSoup(s.text, 'html.parser')
    callrows = soup.select('.element')

    # print(len(callrows))
    callHrefs = []

    # Retrieving the hrefs to all the calls that were posted on this day (Actor's Access recommends you
    # apply on the same day the call is posted).
    for row in callrows:
        regex = re.compile('">\d\d/(\d\d)/\d\d')
        rowDate = re.search(regex, str(row))
        rowDate = rowDate.group(1)
        # print(rowDate, rawDate)
        if rowDate == str(currentDate):
            hrefReg = re.compile('href="(.*)"')
            rowHref = re.search(hrefReg,str(row))
            rowHref = rowHref.group(1)
            rowHref = cleanString(rowHref)
            # print(rowHref)
            callHrefs.append(rowHref)
    # print(len(callHrefs))
    
    # Constructing the casting call page URLs from the retrieved hrefs
    for i,href in enumerate(callHrefs):
        gobacks = (len('region=' + REGIONNUM))
        callHrefs[i] = href[:-gobacks] + '&' + href[-gobacks:]    
    # print("callHrefs: ", callHrefs)

    # Building a list of matched character descriptions which gets returned.
    matchedDescs = []
    if len(callHrefs) == 0:
        print("No calls posted today!")
        return 2
    elif len(callHrefs) == 25:
        print("max number of calls reached, possible misses...")
        dataDict["isMaxCalls"] = True
    print("reading calls...")
    for href in callHrefs:
        # print(href)
        dataDictTuple = readAACall(href,matchedDescs,session)
        dataDict["matchedRoles"] = dataDictTuple[0]
        dataDict["matchedCalls"] = dataDictTuple[1]
    # print(matchedDescs)
    return matchedDescs

# Never got to these :(
def readBackstageCall():
    pass

def parseBackstage():
    pass
