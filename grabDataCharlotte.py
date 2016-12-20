'''
THIS CODE MAY BE INCOMPLETE OR BUGGY
TESTING WAS ONLY ABLE TO BE DONE WITH ONE 
PARCEL ID, SO THIS ENTIRE THING IS MADE ASSUMING
THE ENTIRE WEBSITE WORKS THE SAME AS IT DOES FOR 
THIS ONE PARCEL NUMBER 
'''

import urllib2
from urllib2 import HTTPError
import json
import BeautifulSoup
import HTMLParser
from BeautifulSoup import BeautifulSoup
import csv
from sys import argv
import re

#defines a function to find the line where a certain phrase is
def searchString(string, phrase):
    #begins at line number 1 (0 because we are programming)
    counter = 0
    #goes through each line individually
    for line in string:
        #if searching for a phrase returns an index
        if line.find(phrase) != -1:
            #return the line number where it was found
            return counter
        #otherwise go to the next line
        counter += 1

def makeRow(PRN):
    #an opener is an object that opens files. This is needed so that you can transfer information (like the cookie) when opening the file
    opener = urllib2.build_opener()
    #look at documentation for acquiring the cookie to learn how I got this
    opener.addheaders.append(('Cookie', 'ASP.NET_SessionId=zvxa1oyqwvewvwisn11s1lxf; _ga=GA1.2.1653561520.1481905536; _gat=1'))
    #search uses + instead of - for parcel numbers, so all - are replaced by + in a new variable
    searchPRN = PRN.replace("-","+")
    #split the parcel id into 3 parts because they are useful separate
    PRNParts = PRN.split('-')
    #open website (+PRN allows the website to be different for every parcel id). f.read() returns the html of the page. I copy the 
    #html to result.html in the hexagon directory to figure out what page the program returned
    f = opener.open('http://www.charlottecountypropertycards.com/index.php?mode=search&term='+searchPRN)
    #BeautifulSoup removes all html elements, leaving just the text
    soup = BeautifulSoup(f)
    #because BeautifulSoup returns a list of lines, this line makes it into one big string
    all_textEmptyLines = ''.join(soup.findAll(text=True))
    #removes all empty lines
    all_text = "\n".join([ll.rstrip() for ll in all_textEmptyLines.splitlines() if ll.strip()])
    #changes all text to a list of lines
    splitLinesText = all_text.splitlines()
    #look for a string that matches the pattern: first part of parcel id, any amount of spaces and -'s, followed by the second
    #part of the parcel id, followed by any amound of spaces and -'s, finished with the last part of the parcel id and an "H"
    #because the thing on all_text after the PRN is "House #", so ending it with an H makes it so there can't be anything after
    #the PRN (like a '-A')
    beginningString = re.search(PRNParts[0] + '(-| )*' + PRNParts[1] + '(-| )*' + PRNParts[2] + 'H',all_text).group() 
    #uses searchString function to find line where the PRN is 
    accountNameIndex = searchString(splitLinesText, beginningString)
    #using the index of line, it gets the contents of that line
    accountNameLine = splitLinesText[accountNameIndex-1]
    #if mailing address is a PO BOX
    if(accountNameLine.find("PO BOX") != -1):
        #searches for any combination of letters and spaces followed by "PO BOX", and removes the last 6 digits of the string
        #which would be "PO BOX"
        accountName = re.search("([A-Z]|[a-z]| )*PO BOX",accountNameLine).group()[:-6]
    #if mailing address is a normal address
    else:
        #takes the start of the line, the numbers following "Record: ", the account Name, then the address number,
        #removes "Record: " and all of the numbers, which just leaves the person's name
        accountName = re.sub('\d', '', re.search("Record: ([0-9])*(([A-Z]|[a-z]| )*([0-9])*)",accountNameLine).group()[8:])
    
    #because address directly follows account name, it finds a string starting with the account name, and takes the rest of the 
    #line, then removes the account name from the string leaving the address
    address1Index = searchString(splitLinesText, beginningString)
    address1Line = splitLinesText [address1Index-1]
    address1 = re.search(accountName + "([0-9]| |[a-z]|[A-Z])*", address1Line).group()[len(accountName):]

    address2 = ""

    comboAddress = address1 + ", " + address2
    #site address is split into number and road, so it takes the contents around it so python knows what it is looking for
    #then it removes everything that isnt the number and road, and finally combines the two to make a site address
    siteAddressIndex = searchString(splitLinesText, beginningString)
    siteAddressLine = splitLinesText[siteAddressIndex]
    number = re.search('House #: ([0-9]*)', siteAddressLine).group()[8:]
    road = re.search('Road: ([a-z]|[A-Z]| )*Desc', siteAddressLine).group()[6:][:-4]
    siteAddress = number + " " + road

    
    print(PRN)
    print(address1)
    print(address2)
    print(comboAddress)
    print(siteAddress)
    print(accountName)
    #puts all the values into a list
    myList = [PRN,address1,address2,comboAddress,siteAddress,accountName]
    #makes that list the return value of the function
    return(myList)
  
#when you run the program you say "python grabDataCharlotte.py PRNs.txt CharlotteCounty.csv". This sets script = grabDataCharlotte.py 
#filename = PRNs.txt. and output = CharlotteCounty.csv
script, filename, output = argv
#opens the list of parcel numbers
txt = open(filename).read()
#makes a list of parcel numbers out of the file inputted. Each line is a parcel and THE FIRST LINE IS IGNORED
PRNs = txt.split('\n')[1:]

#sets the file to write to as the output file
filename = output
#opens the file in order to write in it
with open(filename, 'wb') as myFile:
    #makes a list of headers
    myList = ["PRN", "Address_1", "Address_2", "comboaddress", "SiteAddress", "Owner"]
    #makes a writer object
    wr = csv.writer(myFile, quoting=csv.QUOTE_ALL)
    #write the headers
    wr.writerow(myList)
    #loop through every parcel number from the file and runs the makeRow function
    for PRN in PRNs:
        #only makes a new row is the PRN variable has a value in it 
        if PRN != "":
            #sets row variable to be the return value of makeRow
            row = makeRow(PRN)
            #writes the row to the next line of the csv
            wr.writerow(row)

