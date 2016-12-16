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
    try:
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
        
        f = opener.open('https://beacon.schneidercorp.com/Application.aspx?AppID=71&LayerID=592&PageTypeID=4&PageID=490&Q=1686898703&KeyValue=' + PRN)
        
        #no need to update uselessPart. It is the same regardless of the GPIN (parcel ID)
        soup = BeautifulSoup(f)
        all_textEmptyLines = ''.join(soup.findAll(text=True))
        all_text = "\n".join([ll.rstrip() for ll in all_textEmptyLines.splitlines() if ll.strip()])
        
        accountNameIndex = all_text.find("Owners\n")
        accountNameAndTheRest = all_text[accountNameIndex:]
        accountName = accountNameAndTheRest.splitlines()[1].strip().replace("&amp","&")
        
        
        address1Index = all_text.find("Owners\n")
        address1AndTheRest = all_text[address1Index:]
        address1 = address1AndTheRest.splitlines()[2].strip()
        '''
        address2Index = all_text.find("City_State_ZIP_Current")
        address2AndTheRest = all_text[address2Index:]
        address2 = address2AndTheRest.splitlines()[1].strip().replace("COLOR", ""))[0]
        
        address1 = ""
        '''
        address2 = ""

        comboAddress = address1 + ", " + address2

        siteAddressIndex = all_text.find("Property Address")
        siteAddressAndTheRest = all_text[siteAddressIndex:]
        siteAddress = siteAddressAndTheRest.splitlines()[1].strip().replace("No data to display","").replace("Township", "")

        '''
        zoningIndex = all_text.find("Zoning")
        zoningAndTheRest = all_text[zoningIndex:]
        zoning = zoningAndTheRest.splitlines()[1].strip()
        
        
        print(PRN)
        print(address1)
        print(address2)
        print(comboAddress)
        print(siteAddress)
        #print(zoning)
        print(accountName)
        '''
        myList = [PRN,address1,address2,comboAddress,siteAddress,accountName]
        print("success")
        return(myList)
    except IndexError:
        print(PRN + " did not work")
        return [PRN, "","","","",""]
    

script, filename = argv
txt = open(filename).read()
PRNs = txt.split('\n')[1:]
filename = 'Ogle County Failures 2.csv'
with open(filename, 'wb') as myFile:
    myList = ["PRN", "Address_1", "Address_2", "comboaddress", "SiteAddress", "Owner"]
    wr = csv.writer(myFile, quoting=csv.QUOTE_ALL)
    wr.writerow(myList)
    for PRN in PRNs:
        if PRN != "":
            row = makeRow(PRN)
            wr.writerow(row)

