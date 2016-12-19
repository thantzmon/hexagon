import urllib2
from urllib2 import HTTPError
import json
import BeautifulSoup
import HTMLParser
from BeautifulSoup import BeautifulSoup
import csv
from sys import argv
import re

'''
This is just the file from the most recent county. I try to allow this to be the file that can be broken at times, and 
I use all the other files as examples of working code. Try to use this when extending to other counties and then when 
you get it to work, copy the working file to grabData[CountyName].py. All the code below will be explained in other files. 
This is just a playground.
'''


def searchString(string, phrase):
    counter = 0
    for line in string:
        if line.find(phrase) != -1:
            return counter
        counter += 1

def makeRow(PRN):
    PRN = "042-A-55"
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'ASP.NET_SessionId=zvxa1oyqwvewvwisn11s1lxf; _ga=GA1.2.1653561520.1481905536; _gat=1'))
    '''
    ' RETREIVING COOKIE: (note: this is how to do it on Firefox. Chrome, Safari, or others probably have a similar yet different process to do this)
    ' To get your cookie, open the network tab of inspect element and press reload if you have to
    ' Then press the "Accept" or "I agree" or whatever button brings you to the next page
    ' The first value on the spreadsheet should be a POST method from disclaimer 
    ' Under the "Headers" tab you should be able to find a box that says "Cookie" with its correcsponding value
    ' That is the cookie for the website. Put it as the second parameter of the function above.
    '''



    #site address = SITE_ADD_1
    #owner = name
    #mail address = address2 
    #city state zip = SITE_ADD_3
    searchPRN = PRN.replace("-","+")
    PRNParts = PRN.split('-')
    f = opener.open('http://www.charlottecountypropertycards.com/index.php?mode=search&term='+searchPRN)
    #no need to update uselessPart. It is the same regardless of the GPIN (parcel ID)
    soup = BeautifulSoup(f)
    all_textEmptyLines = ''.join(soup.findAll(text=True))
    all_text = "\n".join([ll.rstrip() for ll in all_textEmptyLines.splitlines() if ll.strip()])
    splitLinesText = all_text.splitlines()

    beginningString = re.search(PRNParts[0] + '(-| )*' + PRNParts[1] + '(-| )*' + PRNParts[2] ,all_text).group() 

    accountNameIndex = searchString(splitLinesText, beginningString)
    accountNameLine = splitLinesText[accountNameIndex-1]
    if(accountNameLine.find("PO BOX") != -1):
        #if mailing address is a PO BOX
        accountName = re.search("([A-Z]|[a-z]| )*PO BOX",accountNameLine).group()[:-6]
    else:
        #if mailing address is a normal address
        accountName = re.sub('\d', '', re.search("Record: ([0-9])*(([A-Z]|[a-z]| )*([0-9])*)",accountNameLine).group()[8:])
    
    
    address1Index = searchString(splitLinesText, beginningString)
    address1Line = splitLinesText [address1Index-1]
    address1 = re.search(accountName + "([0-9]| |[a-z]|[A-Z])*", address1Line).group()[len(accountName):]

    '''
    address2Index = all_text.find("City_State_ZIP_Current")
    address2AndTheRest = all_text[address2Index:]
    address2 = address2AndTheRest.splitlines()[1].strip().replace("COLOR", ""))[0]
    
    address1 = ""
    '''
    address2 = ""

    comboAddress = address1 + ", " + address2

    siteAddressIndex = searchString(splitLinesText, beginningString)
    siteAddressLine = splitLinesText[siteAddressIndex]
    number = re.search('House #: ([0-9]*)', siteAddressLine).group()[8:]
    road = re.search('Road: ([a-z]|[A-Z]| )*Desc', siteAddressLine).group()[6:][:-4]
    siteAddress = number + " " + road

    '''
    zoningIndex = all_text.find("Zoning")
    zoningAndTheRest = all_text[zoningIndex:]
    zoning = zoningAndTheRest.splitlines()[1].strip()
    '''
    
    print(PRN)
    print(address1)
    print(address2)
    print(comboAddress)
    print(siteAddress)
    #print(zoning)
    print(accountName)
    
    myList = [PRN,address1,address2,comboAddress,siteAddress,accountName]
    return(myList)
  
makeRow("042-A-55")  
'''
script, filename = argv
txt = open(filename).read()
PRNs = txt.split('\n')[1:]
filename = 'test.csv'
with open(filename, 'wb') as myFile:
    myList = ["PRN", "Address_1", "Address_2", "comboaddress", "SiteAddress", "Owner"]
    wr = csv.writer(myFile, quoting=csv.QUOTE_ALL)
    wr.writerow(myList)
    for PRN in PRNs:
        if PRN != "":
            row = makeRow(PRN)
            wr.writerow(row)
'''
