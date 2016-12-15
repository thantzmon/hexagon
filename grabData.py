import urllib2
import json
import BeautifulSoup
import HTMLParser
from BeautifulSoup import BeautifulSoup
import csv
from sys import argv


def makeRow(PRN):
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'ASP.NET_SessionId=sq3i0tfx3xynu3wvu4f1etxz'))
    f = opener.open("http://mecklenburg.cama.concisesystems.com/PropertyPage.aspx?id=" + PRN)

    soup = BeautifulSoup(f)
    all_textEmptyLines = ''.join(soup.findAll(text=True))
    all_text = text = "\n".join([ll.rstrip() for ll in all_textEmptyLines.splitlines() if ll.strip()])
    accountNameIndex = all_text.find("Account Name")
    accountNameAndTheRest = all_text[accountNameIndex:]
    accountName = accountNameAndTheRest.splitlines()[1].strip().replace("&amp","&")

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


    print(PRN)
    print(address1)
    print(address2)
    print(comboAddress)
    print(siteAddress)
    print(zoning)
    print(accountName)
    myList = [PRN,address1,address2,comboAddress,siteAddress,zoning,accountName]
    return(myList)

script, filename = argv
txt = open(filename)
PRNs = txt.read().split('\r\n')[1:]

with open(filename, 'wb') as myFile:
    myList = ["PRN", "Address_1", "Address_2", "comboaddress", "SiteAddress", "Zoning", "Owner"]
    wr = csv.writer(myFile, quoting=csv.QUOTE_ALL)
    wr.writerow(myList)
    for PRN in PRNs:
        row = makeRow(PRN)
        wr.writerow(row)




