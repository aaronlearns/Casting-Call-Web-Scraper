from datetime import datetime

totalDateTime = str(datetime.now()) # datetime object which is split into two variables.
rawDigitsTime = totalDateTime[11:]
rawDigitsDate = totalDateTime[:10]
# print("rawDigitsDate: ",rawDigitsDate)
rawDate = rawDigitsDate[-2:]
# print(rawDigitsDate[-2:])


dataDict = {
    "ID" : None
    ,
    "date" : rawDigitsDate
    ,
    "time" : rawDigitsTime
    ,
    "forDate" : rawDate
    ,
    "isMaxCalls" : False # This can read up to 25 calls on ActorsAccess. Did we reach that?
    ,
    "matchedRoles" : 0
    ,
    "matchedCalls" : 0
}

REGIONURLS = {
    'LOS ANGELES' : '1',
    'CHICAGO' : '4',
    'South Central' : '7',
    'Southeast' : '9',
    'Pacific (Hawaii)' : '8',
    'Rocky Mountains' : '10',
    'Northwest' : '11',
    'Central Atlantic' : '12',
    'Atlantic Canada' : '13',
    'Alberta' : '14',
    'Canadian Praries' : '16',
    'Midwest' : '19',
    'New England' : '20',
    'North Central' : '21',
    'Northwest Territories' : '22',
    'Nunavut' : '23',
    'Quebec' : '24',
    'San Francisco / NorCal' : '25',
    'TORONTO' : '26',
    'VANCOUVER' : '27',
    'Yukon' : '28',
    'NEW YORK' : '32',
}
USERREGION = "NEW YORK"
USERRACE = ["white", "caucasian"]
USERAGE = range(17,26)
# print(USERAGE)
USERGENDER = ["male","man"]
USERVARS = [USERRACE,USERGENDER,USERAGE]

REGIONNUM = REGIONURLS[USERREGION]

ROOTURL = "https://actorsaccess.com"
