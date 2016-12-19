#these are just importing functions from other python libraries. It doesn't hurt to have them so in my opinion, never delete them.
import urllib2
import json
import BeautifulSoup
import HTMLParser
from BeautifulSoup import BeautifulSoup
import csv
from sys import argv


def makeRow(PRN):
    #an opener is an object that opens files. This is needed so that you can transfer information (like the cookie) when opening the file
    opener = urllib2.build_opener()
    #look at documentation for acquiring the cookie to learn how I got this
    opener.addheaders.append(('Cookie', 'ASP.NET_SessionId=sq3i0tfx3xynu3wvu4f1etxz'))
    #open website (+PRN allows the website to be different for every parcel id). f.read() returns the html of the page. I copy the 
    #html to result.html in the hexagon directory to figure out what page the program returned
    f = opener.open("http://mecklenburg.cama.concisesystems.com/PropertyPage.aspx?id=" + PRN)
    #BeautifulSoup removes all html elements, leaving just the text
    soup = BeautifulSoup(f)
    #because BeautifulSoup returns a list of lines, this line makes it into one big string
    all_textEmptyLines = ''.join(soup.findAll(text=True))
    #removes all empty lines
    all_text = "\n".join([ll.rstrip() for ll in all_textEmptyLines.splitlines() if ll.strip()])
    
    #find the index where the phrase "Account Name" is in all_text. The line under it should be the actual account name.
    accountNameIndex = all_text.find("Account Name")
    #using the index of the phrase "Account Name", removes everything before it in order to make the first line "Account Name"
    #and the second line the account name. This allows us to know what line number the information we want is on.
    accountNameAndTheRest = all_text[accountNameIndex:]
    #makes the string a list of lines, takes the second line, removes all white space, and in the situations where there was an 
    #"&" in the account name, it changes the strange return value of it to a normal &
    accountName = accountNameAndTheRest.splitlines()[1].strip().replace("&amp","&")

    #the next lines do the same thing except with their respective fields
    address1Index = all_text.find("Address1")
    address1AndTheRest = all_text[address1Index:]
    address1 = address1AndTheRest.splitlines()[1].strip()

    address2Index = all_text.find("City, State Zip")
    address2AndTheRest = all_text[address2Index:]
    address2 = address2AndTheRest.splitlines()[1].strip()

    comboAddress = address1 + ", " + address2

    siteAddressIndex = all_text.find("Location Address(es)")
    siteAddressAndTheRest = all_text[siteAddressIndex:]
    siteAddress = siteAddressAndTheRest.splitlines()[1].strip().replace("No data to display","")

    zoningIndex = all_text.find("Zoning")
    zoningAndTheRest = all_text[zoningIndex:]
    zoning = zoningAndTheRest.splitlines()[1].strip()

    #printing all of the fields doesn't actually do anything. I just have it there because I like to make sure that I'm getting 
    #reasonable vales
    print(PRN)
    print(address1)
    print(address2)
    print(comboAddress)
    print(siteAddress)
    print(zoning)
    print(accountName)
    #puts all the values into a list
    myList = [PRN,address1,address2,comboAddress,siteAddress,zoning,accountName]
    #makes that list the return value of the function
    return(myList)

#when you run the program you say "python grabDataMecklenburg.py PRNs.csv". This sets script = grabDataMecklenburg.py and 
#filename = PRNs.csv. Unlike most of the other programs, this takes a csv file with only the parcel numbers inputted and it
#completes the rest of the csv for you
script, filename = argv
#opens the list of parcel numbers
txt = open(filename)
#makes a list of parcel numbers out of the file inputted. Each line is a parcel and THE FIRST LINE IS IGNORED
PRNs = txt.read().split('\r\n')[1:]

#opens the file in order to write in it
with open(filename, 'wb') as myFile:
    #makes a list of headers
    myList = ["PRN", "Address_1", "Address_2", "comboaddress", "SiteAddress", "Zoning", "Owner"]
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