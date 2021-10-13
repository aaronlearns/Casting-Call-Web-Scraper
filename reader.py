import re
import math

from helpers import cleanString
from parsers import USERVARS

# ORDER IS ALWAYS [RACE, GENDER, AGE]

# Quick sort, modified to sort re.match objects by position in string.
# ||| vvvvv |||
def swap(parent,firstPos,secondPos):
    # print("firstPos: ",firstPos,"secondPos: ",secondPos)
    tmp = parent[firstPos]
    parent[firstPos] = parent[secondPos]
    parent[secondPos] = tmp

def M_partition(A,start,end):
    def correctType(obj):
        # print(type(obj))   
        useBool = type(obj) == re.Match
        if not useBool:
            raise ValueError("M_Quicksort may only be used on a list of match objects!")
        else:
            return obj
    # print(A[end][0])
    correctType(A[end][0])
    pivot = A[end][0].start()
    pIndex = start
    for i in range(start,end):
        matchObject = correctType(A[i][0])
        if matchObject.start() <= pivot:
            swap(A,i,pIndex)
            pIndex += 1
    swap(A,pIndex,end)
    return pIndex

def M_quicksort(A,start,end):
    if start >= end: return
    elif start < end:
        pIndex = M_partition(A,start,end)
        M_quicksort(A,start,pIndex-1)
        M_quicksort(A,pIndex+1,end)

# ||| ^^^^^ ||| End quicksort

def deleteListDuplicates(a):
    a = sorted(set(a))
    return list(a)
# testList = [4,4,2,6,3,5]
# print(deleteListDuplicates(testList))

def doListsIntersect(a, b):
    intersect = list(set(a) & set(b))
    # print(intersect)
    # print("a: ", a, "b: ", b)
    return len(intersect) > 0
# first = [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
# second = [17,18,19,20,21,22,23,24,25]
# print(doListsIntersect(first,second))

"""
shiftRegexLists akes a in-list of regular expressions (regexes) 
and appends all matches from a parent string to an outlist.

Each element in the outlist is a list in its own, the first element being the match
object, and the second being the index of the regex in the inList that made the match.
A typical output may look like this:

[[<re.Match object; span=(0, 8), match='15 to 25'>, 1],
[<re.Match object; span=(6, 18), match='25 years old'>, 4],
[<re.Match object; span=(0, 2), match='15'>, 5],
[<re.Match object; span=(6, 8), match='25'>, 5]]

returnGroup argument instead makes the out-list consist of the matching strings
themselves, without the type or match object. This is mostly useless but it can
simplify things and it's only 2 lines of code.

The index of the regex in the original in-list may also be called the regex type.
removableTypes allows you to select certain regexes in the in-list
who's matches will be deleted if an earlier type is matched. For example, for
removableTypes=[1,2], matches produced by the second and third regexes in the
in-list will be deleted if the first regex produces a match, but not if the
fourth does.
"""
def shiftRegexLists(inList, parentString, returnGroup=False, removableTypes=[]):
    outList = []
    for i,reg in enumerate(inList):
        # print(reg)
        regex = re.compile(reg)
        regexIter = regex.finditer(parentString)
        for m in regexIter:
            if returnGroup: outList.append(m.group())
            else: outList.append([m,i])
        if len(removableTypes) > 0:
            for i,result in enumerate(outList[:]):
                typeOfResult = result[1]
                if typeOfResult in removableTypes:
                    for j,otherResult in enumerate(outList[:]):
                        typeOfOtherResult = otherResult[1]
                        if i == j:
                            continue
                        elif typeOfOtherResult < typeOfResult:
                            # print("removing {}".format(result))
                            if len(outList) > 1: outList.remove(result)
                            break
    # print(outList)
    return outList
    # print(desc)

# The regex lists order the matches the reader searches for. Regexes with a ^ next to them
# are listed in the removableTypes when shiftRegexLists is called.

genderRegs = [

"(f?e?male)", # 'male' and/or 'female'

"\s([wW]?o?[mM]an)", # woman and/or man^

" ?(s?he) ", # pronouns^

"([nN]on[-\s]?[bB]inary)"] # The term "non-binary"



raceRegs = [

# Cases including the word "ethnicity", these are most common on actors access
"(a[ny|l]{2} ethnicit[y|ies]{1,3})", "(open ethncicity)","(mixed ethnicit[y|ies]{1,3})",

# Colloquial terms which refer to race
"(white)", "(caucasian)", "(black)", "\s(asian)","(latin[oax])","(hispanic)",

# Continents
"(african)","(european)",

# Nations / Regions
"(chinese)","(japanese)","(korean)","(filipino)","(dominican)","(cuban)","(mexican)","(carribean)",
"(pacific islander)","(hawaiian)","(nuyorican)",

# Geographical locations hypenated with "American" and other hypenations
"(middle[-|\s]eastern)","(\w+[-|\s]american)",

# Acronyms
"(aapi)","(b?i?poc)",

# Other
"(\w+ of color)"]

# In the ageRegs list, earlier matches are privileged, so the order is important.
ageRegs = ["(\d0)['|’]?s", # Age written as (numerically) "thirties"

"(\d\d*)[\s\-*t?o?]+(\d\d*)", # Age written explicitly as between two numbers

"(\d{1,2})\s*\+", # Age written as a number or higher e.g. "18+"

"(\d\d*).{2,5}to play \d\d*", # Age for character separate from actor e.g. "18+ to play 15"

"[^\s-]*?(\d\d*) years old", # Age written as a number of "years old"

"(\d\d*)", # Age written as a number^

# Age written as a colloquial term^ (TODO: ADD 'middle aged' to this and algo)
"(teenager)","(middle[-\s]aged?)"] 


# ||| vvv GENDER vvv |||
def getDescGenders(desc):
    descGenders = shiftRegexLists(genderRegs, desc,removableTypes=[1,2])
    # print(descGenders)
    M_quicksort(descGenders,0,len(descGenders)-1)
    for result in descGenders:
        matchObject = result[0]
        result[0] = matchObject.group(1)
    for i,result in enumerate(descGenders):
        descGenders[i] = result[0]
    return descGenders
            
# ||| ^^^ GENDER ^^^ |||

# ||| vvv RACE vvv |||
def getDescRace(desc):
    descRaces = shiftRegexLists(raceRegs,desc)
    # print("descRaces: ", descRaces)
    M_quicksort(descRaces,0,len(descRaces)-1)
    # print("descRaces: ", descRaces)
    for i,result in enumerate(descRaces):
        m = result[0]
        descRaces[i] = m.group(1)
        # print("descRaces: ", descRaces)
    return descRaces

# ||| ^^^ RACE ^^^ |||



# ||| vvv AGE vvv |||
def getDescAgeRange(desc):
    descAgeRaw = shiftRegexLists(ageRegs, desc, removableTypes=range(3,8))
    # print(descAgeRaw)
    M_quicksort(descAgeRaw,0,len(descAgeRaw)-1)
    # print(descAgeRaw)
    descAgeRange = []
    if descAgeRaw:
        # print(descAgeRaw[0][0])
        # print(descAgeRaw)
        m = descAgeRaw[0]
        # print("beg: ", beg)
        hisAndLos = []
        descAgeRaw = [descAgeRaw[0]]
        for result in descAgeRaw:
            m = result[0]
            # print(m)
            beg = m.start()
            regexType = result[1]
            lo = int(m.group(1))
            hi = 0 
            if regexType == 0:
                hi = lo + 10
                if desc[beg - 6: beg] == "early ":
                    hi = hi - 5
                    # print('early')
                elif desc[beg - 5: beg] == "late ":
                    lo = lo + 6
                    # print('late')
                elif desc[beg - 4: beg] == "mid ":
                    lo = lo + 4
                    hi = hi - 3
                    # print('mid')
            elif regexType == 1:
                hi = m.group(2)
            elif regexType == 2:
                hi = (int(lo) * 2) - 7
            elif regexType in [3,4,5] and beg < 50:
                hi = lo + 3
                lo = lo - 3
            elif regexType == 6:
                lo = 13
                hi = 19
            elif regexType == 7:
                lo = 45
                hi = 65

            if lo and hi:
                lo = int(lo)
                hi = int(hi)
                # print("lo:",lo,"hi:",hi)
                hisAndLos.append(lo)
                hisAndLos.append(hi)
        # print(hisAndLos)
        if hisAndLos:
            hisAndLos = sorted(hisAndLos)
            kingHi = hisAndLos[-1]
            kingLo = hisAndLos[0]

            # This would do some odd math to "soften" the boundaries of already large ranges.
            # TODO MMDIP

            # difference = (kingHi - kingLo)
            # if difference >= 10:
            #     rootRatio = .835
            #     # print("rootRatio:",rootRatio)
            #     diffRoot = math.floor(difference**rootRatio)
            #     average = math.floor((kingLo + kingHi) / 2)
            #     kingHi = average + diffRoot
            #     kingLo = average - diffRoot
            descAgeRange = range(kingLo,kingHi+1)
    # print(descAgeRange)
    return descAgeRange
        
# ||| ^^^ AGE ^^^ |||

def getDescData(desc):
    # print(desc)
    desc = desc.lower()
    descRaces = getDescRace(desc)
    descGenders = getDescGenders(desc)
    descAgeRange = getDescAgeRange(desc)

    finalList = [descRaces,descGenders,descAgeRange]
    for i,li in enumerate(finalList):
        # print(li)
        finalList[i]= deleteListDuplicates(li)
    # print(finalList,"\n")
    return finalList

def descUserMatched(userData, desc):
    descData = getDescData(desc)
    # print("descData: ", descData, "userData: ", userData)
    matches = ["RACE","GENDER","AGE"]
    for i,li in enumerate(descData):    
        if len(li) == 0:
            # print("didn't get any data for {}".format(matches[i]))
            matches[i] = True
        else:
            # print("li: ", li, "userData[i]: ", userData[i])
            # print("doListsIntersect: ", doListsIntersect(li,userData[i]))
            matches[i] = doListsIntersect(li,userData[i])
    descRace = descData[0]
    if ('all ethnicities' in descRace) or ('any ethnicity' in descRace) or ("open ethnicity" in descRace):
        matches[0] = True
    # print(matches)
    userM = all(matches)
    # if userM:print('desc matched for user')
    return userM

testDescs = {
1 : "Playing age 18 to 40 years old, all ethnicities female. Sensational singer/actor/dancers required to perform the SIX wives of Henry VIII as they reunite to tell their stories in the form of a pop concert."
,
2 : "Males, late 20's – early 30's, To cover the onstage ensemble factory workers, the featured ensemble roles of the ANGELS, and possibly principal roles. Must be terrific dancers, singers and actors. [Ensemble]"
,
3 : "all ethnicities male or female. Seeking NON-UNION with Cars AND a 2nd person (friend, family, roommate, buddy) to work TOGETHER as driver and passenger on camera! BOTH people should have valid driver's license and be able to drive the (1) car in case either needs to move the car at any point. This work will primarily be in the car for a traffic jam scene, so you should be comfortable being together in the car for lengths of time. NO red or white cars! COVID test on Mon 6/14 in Brooklyn Works Tuesday 6/15 exterior in Manhattan *Will be a scene with over 100 bg, but will all be exterior and spaced out, and you will be in your car!* When submitting, please include a note with the make, model, year, and color of your car AND confirm you have a 2nd person to work with you! *IF YOU DO NOT INCLUDE THIS NOTE, WE WILL NOT REACH OUT TO YOU!*"
,
4 : "To play/cover male-identified characters, 20's - 30's, any/all ethnicities. NEED MORE SUBMISSIONS OF 5'11\" OR TALLER. Highly skilled dancers with impeccable ballet technique. All must sing very well. Partnering skills a must. Possible principal understudy assignments. ENSEMBLE. Featured ensemble roles of SIEGFRIED and VON ROTHBART will also come out of the ensemble. Excellent partners with extensive lifting experience/ability, and leaping ability/technique."
,
5 : "19 to 26 years old, African, Black male. Clean cut, medium height. Chris is shadowing alongside nurse Michelle at the hospital to fulfill his clinicals. He is unsure of himself and perhaps appears younger than his age. LEAD"
,
6 : "25 to 30 years old, all ethnicities male. Cassius' co-worker at the sanitation department. Tries to give Cassius his space but also fearful he may be too old for the job."
,
7 : "28-32 years old, Black male, who carries himself like a seasoned dancer but he is working as a waiter in this LGBT domestic drama. Andrew is a very submissive man in an abusive relationship. Andrew meets a fresh faced Midwestern guy named Bradley at work and over the course of 6 months they fall in love. The role requires strong dramatic acting skills and solid dance movement with the ability to pick up choreography. LEAD"
,
8 : "TINA – Legal 18 (to play 15). Female / Female identifying / Non-Binary. All ethnicities. 5’10”++. Impossibly tall & lanky, Tina has never met a flat surface she couldn’t trip over. In her words: “I move through this world like a drunk baby giraffe.” The queen of physical comedy and one-liners. (SUPPORTING)"
,
9 : "18 to 25 years old, all ethnicities female. We are looking for someone to play a TRUE 18-25 y/o. Must be 5'8\" or taller. PLEASE DO NOT SUBMIT IF YOU ARE UNDER 5'8\". 5'7\" OR BELOW WILL NOT BE CONSIDERED. Very thin. Stunningly GORGEOUS. A high-fashion model. One of the most world-renowned models in the industry. Doesn't care what people think about her. Has all the confidence in the world and owns every room she walks into. Has an edge and a bit of a dark side. This character is revealed to be a serial killer. LOOKING FOR REAL LIFE HIGH FASHION MODELS. **WE ARE NOW ABLE TO FLY THOSE WHO DO NOT LIVE IN NY AND PUT THEM UP. PLEASE SUBMIT OUT OF TOWN TALENT.**"
,
10 : "18 to 30 years old, Black, West Indies/Caribbean, Mixed Ethnicity, Asian, Hispanic male. Open to different looks(dyed hair or anything that fits your personality) Feels like the outcast of the family that always lives in his brother's shadow. Doesn't know he's adopted."
,
11 : '25 to 40 years old, all ethnicities male. Is a man who will spend the first act as a woman so credibly that he will utterly fool both RIP (who will fall for him) and the audience. Has a song that must be sung as a woman. Think "Mary Sunshine". More Female Impersonator than Drag Queen. An actor who can convincingly play a woman. Must be able to sing as a woman.'
,
12 : '20 to 50 years old, female. Strong soprano who moves well ?Neither demanding nor critical, sticks with the rules.'
,
13 : "25 to 35 years old, male. – late 20’s, male. Any ethnicity. Associate editor of The Messenger. He's very well read and always up for a fiery discussion. He loves Petra and his job. He struggles to reconcile his personal and professional loyalties."
,
14 : "LEAD ROLE. 30’s - 40’s.  All ethnicities female. An established antiquities buyer who's evening celebration is suddenly cut short by the male lead. Determined to punish the man who harmed her, she is transformed into the Greek Goddess, Alecto.  She’s sophisticated, independent, and highly educated."
,
15 : "Female, white, 40’s - 50’s, heavyset. An unaccredited teacher, constantly sharing her interest in the occult with her students."
,
16 : "Female, any ethnicity, 20’s - 50’s. A shrinking violet who runs in terror from the school when her students go crazy."
,
17 : "14 to 16 years old, white male. As Brandon ages into his teen years, his quiet and timid side begins to give way to his rebellious side. He begins to see Thomas and the church in a different light. He wonders if what Thomas is preaching is true. Brandon grows conflicted and eventually tries to hatch his escape. LEAD ROLE"
,
18 : 'Male, 40, white, insensitive, Jeff is the station manager at the TV studio where Monica works. Jeff chats with Monica after her recent bereavement  ("So, I’m sure you’re all cried out after your taking two long weeks off"), and gives her advice on how to nab the new solo host job also mentioning her new assistant. Later, Jeff notes that Monica\'s success will reflect well on him too in his mind, consistency is way better than compassion...SUPPORTING'
,
19 : "This waitress at a nice restaurant asks Simone if she can get her something to drink...1 line, 1 scene (82)"
,
20 : "15 to 25 years old, all ethnicities male. Actors who move well. Ballet not required."
,
21 : "50 to 59 years old, all ethnicities male. Roger is a charming, cultured, and lethally smart, “smiling psychopath”. Not your typical looking “bad guy”. A shrewd businessman who definitely owns a well-worn copy of “The 7 Habits of Highly Effective People” - he is the kingpin of a criminal organization that traffics in black market human organs. One minute he’s engaging in friendly banter, and the next he’s calmly and icily threatening to carve your still-beating heart out of your chest if you don’t come up with his money. He constantly dances on the fine line between being infectiously likeable, and wholly terrifying. Roger’s business requires a fair amount of schmoozing and relationship-building, but to him, human beings are nothing more than walking bags of “inventory”. SUPPORTING. Shoots 1-2 days.Please include recognizable talent in your submission for this role."
,
22 : "15 to 18 years old, white male. Frankie will be played by Mario Cantone. This is a flashback scene, where we see him aged 15-18. day player role. Looking for an young actor who can look like Mario CantoneSeason 2, Episode 4."
,
23 : "19 to 27 years old, all ethnicities male or female. Athletic with a strong yoga background but does NOT need to be advanced.\nMinimal tattoos.\nMust fit into our sample sizes\nFemale:Bottom + Top: Small & Shoe: 7 US\nMale: Bottom + Top: Medium & Shoe: 9 US\n"
,
24 : "18 to 35 years old, all ethnicities male or female. Presents Athletic. A militia comprised of extremely athletic people who use their background in martial arts, parkour, and gymnastics to navigate the the infected landscape. EXTRA\n$150 per day."
,
25 : "Doubles as Kalid. 24 to 30 years old, Middle Eastern male. Strong and good looking. Youssef's natural son, Front Desk Security. In love with and to be married to Alisha. Murdered by ISIS. (KALID)-a new recruit to ISIS has converted to Muslim. Must prove himself to al-Zumani."
,
26 : "30 to 40 years old, white male. Tied himself to a tree for the environment. Has been there a while and is disheveled."
,
27: "25 to 35 years old, male. Think Madmen Ambitious. Charismatic. Cynical. Great hair. With a chip on his shoulder, Jack is a high-powered advertising executive gunning for his next score. Smooth with the ladies and emotionally distant, he’s not the guy you’d peg to don a red velvet suit and pass out toys to girls and boys. Jack goes from our anti-hero to our hero. Strong crooning tenor and ability to dance."
}


example = USERVARS
single = testDescs[27]
single = cleanString(single)
# print(descUserMatched(example, single))

def descUserMatchedTest():
    corrects = [False,False,True,True,False,False,False,False, #8
    False,False,False,False,False,False,False,False,False,False, #18
    False,True,False,True,True,True,False] #25
    dictLen = len(corrects)
    for n in range(1, dictLen + 1):
        result = descUserMatched(example, testDescs[n])
        
        # print(f"testDesc[{n}]: ", result)

        try: assert(result == corrects[n-1])
        except AssertionError:
            print("Failed on desc[{}].".format(n))
            break
        if n == dictLen:print("Pass!")
# descUserMatchedTest()