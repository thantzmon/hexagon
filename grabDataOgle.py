import urllib2
from urllib2 import HTTPError
import json
import BeautifulSoup
import HTMLParser
from BeautifulSoup import BeautifulSoup
import csv
from sys import argv
import re



def makeRow(PRN):
    #in the case of an error, this will make the program not crash, therefore this chunk of code only runs when no error happens
    try:
        #an opener is an object that opens files. This is needed so that you can transfer information (like the cookie) when opening the file
        opener = urllib2.build_opener()
        #look at documentation for acquiring the cookie to learn how I got this
        opener.addheaders.append(('Cookie', 'ASP.NET_SessionId=zvxa1oyqwvewvwisn11s1lxf; _ga=GA1.2.1653561520.1481905536; _gat=1'))
        #look at documentation for acquiring the correct website to learn how I got this
        f = opener.open('https://beacon.schneidercorp.com/Application.aspx?AppID=71&LayerID=592&PageTypeID=4&PageID=490&Q=1686898703&KeyValue=' + PRN)
        #BeautifulSoup removes all html elements, leaving just the text
        soup = BeautifulSoup(f)
        #because BeautifulSoup returns a list of lines, this line makes it into one big string
        all_textEmptyLines = ''.join(soup.findAll(text=True))
        #removes all empty lines
        all_text = "\n".join([ll.rstrip() for ll in all_textEmptyLines.splitlines() if ll.strip()])
        
        #find the index where the phrase "Owners" followed by a new line is in all_text. The line under it should be the actual 
        #account name.
        accountNameIndex = all_text.find("Owners\n")
        #using the index of the phrase "Owners\n", removes everything before it in order to make the first line "Owners"
        #and the second line the account name. This allows us to know what line number the information we want is on.
        accountNameAndTheRest = all_text[accountNameIndex:]
        #makes the string a list of lines, takes the second line, removes all white space, and in the situations where there was an 
        #"&" in the account name, it changes the strange return value of it to a normal &.
        accountName = accountNameAndTheRest.splitlines()[1].strip().replace("&amp","&")
        
        #the next lines do the same thing except with their respective fields
        address1Index = all_text.find("Owners\n")
        address1AndTheRest = all_text[address1Index:]
        address1 = address1AndTheRest.splitlines()[2].strip()

        address2 = ""

        comboAddress = address1 + ", " + address2

        siteAddressIndex = all_text.find("Property Address")
        siteAddressAndTheRest = all_text[siteAddressIndex:]
        siteAddress = siteAddressAndTheRest.splitlines()[1].strip().replace("No data to display","").replace("Township", "")

        #puts all the values into a list
        myList = [PRN,address1,address2,comboAddress,siteAddress,accountName]
        #confirms the function ended succesfully
        print("success")
        #makes that list the return value of the function
        return(myList)
    #if the program ended with an error (the parcel number is not on the website) it fails without breaking the program
    except IndexError:
        #prints which parcel number failed
        print(PRN + " did not work")
        #returns an empty row to write to the csv
        return [PRN, "","","","",""]
    
#when you run the program you say "python grabDataOgle.py PRNs.txt OgleCounty.csv". This sets script = grabDataOgle.py 
#filename = PRNs.txt. and output = OgleCounty.csv
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

