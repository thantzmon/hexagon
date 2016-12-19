import urllib2
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

        f = opener.open("http://auditor.co.ross.oh.us/Data.aspx?ParcelID=" + PRN)
        soup = BeautifulSoup(f)
        all_textEmptyLines = ''.join(soup.findAll(text=True))
        all_text = "\n".join([ll.rstrip() for ll in all_textEmptyLines.splitlines() if ll.strip()])
        accountNameIndex = all_text.find("Owner:")
        accountNameAndTheRest = all_text[accountNameIndex:]
        accountName = accountNameAndTheRest.splitlines()[1].strip().replace("&amp","&").replace("&nbsp;","")

        firstAddressIndex = all_text.find("Address:")
        firstAddressAndTheRest = all_text[firstAddressIndex:]
        firstAddress = firstAddressAndTheRest.splitlines()[1].strip()

        afterFirstAddressIndex = firstAddressAndTheRest[firstAddressAndTheRest.find(firstAddress):]
        address1Index = afterFirstAddressIndex.find("Address:")
        address1AndTheRest = afterFirstAddressIndex[address1Index:]
        address1 = address1AndTheRest.splitlines()[1].strip().replace("&nbsp;","")

        address2Index = all_text.find("City State Zip:")
        address2AndTheRest = all_text[address2Index:]
        address2 = address2AndTheRest.splitlines()[1].strip().replace("&nbsp;","")

        comboAddress = address1 + ", " + address2

        afterSecondAddressIndex = address1AndTheRest[address1AndTheRest.find(address1):]
        siteAddressIndex = afterSecondAddressIndex.find("Address:")
        siteAddressAndTheRest = afterSecondAddressIndex[siteAddressIndex:]
        siteAddress = siteAddressAndTheRest.splitlines()[1].strip().replace("No data to display","").replace("&nbsp;","")
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
    except IndexError:
        print(PRN + " is not on this website.")
        return([PRN,"","","","",""])

script, filename = argv
txt = open(filename)
PRNs = txt.read().split('\n')[1:]

filename = 'test.csv'
with open(filename, 'wb') as myFile:
    myList = ["PRN", "Address_1", "Address_2", "comboaddress", "SiteAddress", "Owner"]
    wr = csv.writer(myFile, quoting=csv.QUOTE_ALL)
    wr.writerow(myList)
    for PRN in PRNs:
        row = makeRow(PRN)
        wr.writerow(row)




