import urllib2
from urllib2 import HTTPError
import json
import BeautifulSoup
import HTMLParser
from BeautifulSoup import BeautifulSoup
import csv
from sys import argv


def makeRow(PRN):
    #in the case of an error, this will make the program not crash, therefore this chunk of code only runs when no error happens
    try:
        #an opener is an object that opens files. This is needed so that you can transfer information (like the cookie) when opening the file
        opener = urllib2.build_opener()
        #look at documentation for acquiring the cookie to learn how I got this
        opener.addheaders.append(('Cookie', 'ARRAffinity=9ecf3dba050f3416baa0b5328a21cbf6a66854176ad4bc52e895aa32b01b309d; ASP.NET_SessionId=42qje445geirdvamun0t0i55; HasCookies=True; Disclaimer=accept'))
        #look at documentation for acquiring the correct website to learn how I got this
        f = opener.open("http://caplus.myossi.com/gscwebp/search.aspx?&skey=pin&svalue=" + PRN + "&canht=307&canwd=866&boundne=37.020740681886586,-78.82536499023439&boundsw=36.683382714144166,-80.01463500976564")
        #BeautifulSoup removes all html elements, leaving just the text
        soup = BeautifulSoup(f)
        #because BeautifulSoup returns a list of lines, this line makes it into one big string
        all_textEmptyLines = ''.join(soup.findAll(text=True))
        #removes all empty lines
        all_text = "\n".join([ll.rstrip() for ll in all_textEmptyLines.splitlines() if ll.strip()])
        
        #find the index where the phrase "NAME" is in all_text. The line under it should be the actual account name.
        accountNameIndex = all_text.find("NAME")
        #using the index of the phrase "NAME", removes everything before it in order to make the first line "NAME"
        #and the second line the account name. This allows us to know what line number the information we want is on.
        accountNameAndTheRest = all_text[accountNameIndex:]
        #makes the string a list of lines, takes the second line, removes all white space, and in the situations where there was an 
        #"&" in the account name, it changes the strange return value of it to a normal &.
        accountName = accountNameAndTheRest.splitlines()[1].strip().replace("&amp","&")

        #the next lines do the same thing except with their respective fields
        address1Index = all_text.find("ADDRESS")
        address1AndTheRest = all_text[address1Index:]
        address1 = address1AndTheRest.splitlines()[1].strip()

        address2Index = all_text.find("ACCOUNT_CS")
        address2AndTheRest = all_text[address2Index:]
        address2 = address2AndTheRest.splitlines()[1].strip().replace("COLOR", "")

        comboAddress = address1 + ", " + address2

        siteAddressIndex = all_text.find("SITE_ADD_1")
        siteAddressAndTheRest = all_text[siteAddressIndex:]
        siteAddress = siteAddressAndTheRest.splitlines()[1].strip().replace("No data to display","").replace("SITE_ADD_2", "")


        #printing all of the fields doesn't actually do anything. I just have it there because I like to make sure that I'm getting 
        #reasonable vales

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
    #if the program ended with an error (the parcel number is not on the website) it fails without breaking the program
    except (IndexError, urllib2.HTTPError) as e:
        #prints which parcel number failed
        print(PRN + " is not on this website.")
        #returns an empty row to write to the csv
        return([PRN,"","","","",""])

#when you run the program you say "python grabDataPittsylvania.py PRNs.txt". This sets script = grabDataPittsylvania.py and 
#filename = PRNs.txt.
script, filename = argv
#opens the list of parcel numbers
txt = open(filename).read()
#makes a list of parcel numbers out of the file inputted. Each line is a parcel and THE FIRST LINE IS IGNORED
PRNs = txt.split('\n')[1:]

#sets the file to write to as "Pittsylvania County.csv"
filename = 'Pittsylvania County.csv'
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
        #sets row variable to be the return value of makeRow
        row = makeRow(PRN)
        #writes the row to the next line of the csv
        wr.writerow(row)




