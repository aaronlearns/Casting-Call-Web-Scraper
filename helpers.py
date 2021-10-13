
from bs4 import BeautifulSoup

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


# Determines whether a call was posted on the current date
# Takes a get requested page as an argument.
