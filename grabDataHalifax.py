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
    
    f = urllib2.urlopen('https://www.webgis.net/arcgis/rest/services/VA/HalifaxCo_WebGIS/MapServer/10/query?f=json&where=%28GPIN%20=%27' + PRN + '%27%29&returnGeometry=false&spatialRel=esriSpatialRelIntersects&geometryPrecision=1&outFields=*&outSR=102100')
    uselessPart = urllib2.urlopen('https://www.webgis.net/arcgis/rest/services/VA/HalifaxCo_WebGIS/MapServer/10/query?f=json&where=%28PIN%20=%273543-00-1004%27%29&returnGeometry=false&spatialRel=esriSpatialRelIntersects&geometryPrecision=1&outFields=*&outSR=102100')
    #no need to update uselessPart. It is the same regardless of the GPIN (parcel ID)
    soup = BeautifulSoup(f)
    uselessSoup = BeautifulSoup(uselessPart)
    useless_text = ''.join(uselessSoup.findAll(text=True))
    clean_useless_text = "\n".join([ll.rstrip() for ll in useless_text.splitlines() if ll.strip()])
    
    deletableIndex = clean_useless_text.find("features")
    deletable = clean_useless_text[:deletableIndex]


    all_textEmptyLines = ''.join(soup.findAll(text=True))
    all_text = "\n".join([ll.rstrip() for ll in all_textEmptyLines.splitlines() if ll.strip()])
    
    useful_text = all_text.replace(deletable, "").replace(":","\n")

    
    accountNameIndex = useful_text.find("Owner_Current")
    accountNameAndTheRest = useful_text[accountNameIndex:]
    accountName = re.findall('"([^"]*)"', accountNameAndTheRest.splitlines()[1].strip().replace("&amp","&"))[0]

    address1Index = useful_text.find("Address_Line_1_Current")
    address1AndTheRest = useful_text[address1Index:]
    address1 = re.findall('"([^"]*)"', address1AndTheRest.splitlines()[1].strip())[0]

    address2Index = useful_text.find("City_State_ZIP_Current")
    address2AndTheRest = useful_text[address2Index:]
    address2 = re.findall('"([^"]*)"',address2AndTheRest.splitlines()[1].strip().replace("COLOR", ""))[0]

    comboAddress = address1 + ", " + address2

    siteNumberIndex = useful_text.find("Parcel_Location_Number")
    siteNumberAndTheRest = useful_text[siteNumberIndex:]
    siteNumber = re.findall('"([^"]*)"', siteNumberAndTheRest.splitlines()[1].strip().replace("Parcel_Location_Street", ""))[0]
    
    siteStreetIndex = useful_text.find("Parcel_Location_Street")
    siteStreetAndTheRest = useful_text[siteStreetIndex:]
    siteStreet = re.findall('"([^"]*)"',siteStreetAndTheRest.splitlines()[1].strip().replace("Alternate_Parcel_ID", ""))[0]

    siteAddress = siteNumber + " " + siteStreet
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


