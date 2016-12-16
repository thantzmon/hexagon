import urllib2
from urllib2 import HTTPError
import json
import BeautifulSoup
import HTMLParser
from BeautifulSoup import BeautifulSoup
import csv
from sys import argv


def makeRow(PRN):
    try:
        opener = urllib2.build_opener()
        opener.addheaders.append(('Cookie', 'ARRAffinity=9ecf3dba050f3416baa0b5328a21cbf6a66854176ad4bc52e895aa32b01b309d; ASP.NET_SessionId=42qje445geirdvamun0t0i55; HasCookies=True; Disclaimer=accept'))
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
        f = opener.open("http://caplus.myossi.com/gscwebp/search.aspx?&skey=pin&svalue=" + PRN + "&canht=307&canwd=866&boundne=37.020740681886586,-78.82536499023439&boundsw=36.683382714144166,-80.01463500976564")
        soup = BeautifulSoup(f)
        all_textEmptyLines = ''.join(soup.findAll(text=True))
        all_text = text = "\n".join([ll.rstrip() for ll in all_textEmptyLines.splitlines() if ll.strip()])
        accountNameIndex = all_text.find("NAME")
        accountNameAndTheRest = all_text[accountNameIndex:]
        accountName = accountNameAndTheRest.splitlines()[1].strip().replace("&amp","&")

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
    except (IndexError, urllib2.HTTPError) as e:
        print(PRN + " is not on this website.")
        return([PRN,"","","","",""])

script, filename = argv
txt = open(filename).read()
PRNs = txt.split('\n')[1:]
filename = 'test.csv'
with open(filename, 'wb') as myFile:
    myList = ["PRN", "Address_1", "Address_2", "comboaddress", "SiteAddress", "Owner"]
    wr = csv.writer(myFile, quoting=csv.QUOTE_ALL)
    wr.writerow(myList)
    for PRN in PRNs:
        row = makeRow(PRN)
        wr.writerow(row)




