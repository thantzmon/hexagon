import urllib2
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
        #open website (+PRN allows the website to be different for every parcel id). f.read() returns the html of the page. I copy the 
        #html to result.html in the hexagon directory to figure out what page the program returned
        f = opener.open("http://auditor.co.ross.oh.us/Data.aspx?ParcelID=" + PRN)
        #BeautifulSoup removes all html elements, leaving just the text
        soup = BeautifulSoup(f)
        #because BeautifulSoup returns a list of lines, this line makes it into one big string
        all_textEmptyLines = ''.join(soup.findAll(text=True))
        #removes all empty lines
        all_text = "\n".join([ll.rstrip() for ll in all_textEmptyLines.splitlines() if ll.strip()])
        
        #find the index where the phrase "Owner:" is in all_text. The line under it should be the actual account name.
        accountNameIndex = all_text.find("Owner:")
        #using the index of the phrase "Owner:", removes everything before it in order to make the first line "Owner:"
        #and the second line the account name. This allows us to know what line number the information we want is on.
        accountNameAndTheRest = all_text[accountNameIndex:]
        #makes the string a list of lines, takes the second line, removes all white space, and in the situations where there was an 
        #"&" in the account name, it changes the strange return value of it to a normal &. Also changes "&nbsp" (which is similar to
        #a space bar to nothing)
        accountName = accountNameAndTheRest.splitlines()[1].strip().replace("&amp","&").replace("&nbsp;","")

        #in this website, it used the title "Address:" for both mailing address and site address. They also used the word address
        #one time before they actually started writing out the information, so these lines finds the first mention of the phrase
        firstAddressIndex = all_text.find("Address:")
        firstAddressAndTheRest = all_text[firstAddressIndex:]
        firstAddress = firstAddressAndTheRest.splitlines()[1].strip()

        #using the location of the first use of the word address, it takes it out and finds the location of the second occurance
        #of "Address:"
        afterFirstAddressIndex = firstAddressAndTheRest[firstAddressAndTheRest.find(firstAddress):]
        address1Index = afterFirstAddressIndex.find("Address:")
        address1AndTheRest = afterFirstAddressIndex[address1Index:]
        address1 = address1AndTheRest.splitlines()[1].strip().replace("&nbsp;","")

        address2Index = all_text.find("City State Zip:")
        address2AndTheRest = all_text[address2Index:]
        address2 = address2AndTheRest.splitlines()[1].strip().replace("&nbsp;","")

        comboAddress = address1 + ", " + address2

        #does the same as address1, except it removes the second occurance also
        afterSecondAddressIndex = address1AndTheRest[address1AndTheRest.find(address1):]
        siteAddressIndex = afterSecondAddressIndex.find("Address:")
        siteAddressAndTheRest = afterSecondAddressIndex[siteAddressIndex:]
        siteAddress = siteAddressAndTheRest.splitlines()[1].strip().replace("No data to display","").replace("&nbsp;","")

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
    except IndexError:
        #prints which parcel number failed
        print(PRN + " is not on this website.")
        #returns an empty row to write to the csv
        return([PRN,"","","","",""])

#when you run the program you say "python grabDataRoss.py PRNs.txt RossCounty.csv". This sets script = grabDataRoss.py 
#filename = PRNs.txt. and output = RossCounty.csv
script, filename,output = argv
#opens the list of parcel numbers
txt = open(filename)
#makes a list of parcel numbers out of the file inputted. Each line is a parcel and THE FIRST LINE IS IGNORED
PRNs = txt.read().split('\n')[1:]

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
        #sets row variable to be the return value of makeRow
        row = makeRow(PRN)
        #writes the row to the next line of the csv
        wr.writerow(row)




