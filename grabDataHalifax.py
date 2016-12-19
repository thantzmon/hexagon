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
    #an opener is an object that opens files. This is needed so that you can transfer information (like the cookie) when opening the file
    opener = urllib2.build_opener()
    #look at documentation for acquiring the cookie to learn how I got this
    opener.addheaders.append(('Cookie', 'ARRAffinity=9ecf3dba050f3416baa0b5328a21cbf6a66854176ad4bc52e895aa32b01b309d; ASP.NET_SessionId=42qje445geirdvamun0t0i55; HasCookies=True; Disclaimer=accept'))

    #look at documentation for acquiring the correct website to learn how I got this
    f = urllib2.urlopen('https://www.webgis.net/arcgis/rest/services/VA/HalifaxCo_WebGIS/MapServer/10/query?f=json&where=%28GPIN%20=%27' + PRN + '%27%29&returnGeometry=false&spatialRel=esriSpatialRelIntersects&geometryPrecision=1&outFields=*&outSR=102100')
    #look at documentation for acquiring the correct website to learn how I got this
    #no need to update uselessPart. It is the same regardless of the GPIN (parcel ID)
    uselessPart = urllib2.urlopen('https://www.webgis.net/arcgis/rest/services/VA/HalifaxCo_WebGIS/MapServer/10/query?f=json&where=%28PIN%20=%273543-00-1004%27%29&returnGeometry=false&spatialRel=esriSpatialRelIntersects&geometryPrecision=1&outFields=*&outSR=102100')
    #BeautifulSoup removes all html elements, leaving just the text
    soup = BeautifulSoup(f)
    #BeautifulSoup removes all html elements, leaving just the text
    uselessSoup = BeautifulSoup(uselessPart)
    #because BeautifulSoup returns a list of lines, this line makes it into one big string
    useless_text = ''.join(uselessSoup.findAll(text=True))
    #removes all empty lines
    clean_useless_text = "\n".join([ll.rstrip() for ll in useless_text.splitlines() if ll.strip()])
    #finds the index where the useful page and useless page stop being the same
    deletableIndex = clean_useless_text.find("features")
    #find the text to be deleted
    deletable = clean_useless_text[:deletableIndex]

    #because BeautifulSoup returns a list of lines, this line makes it into one big string
    all_textEmptyLines = ''.join(soup.findAll(text=True))
    #removes all empty lines
    all_text = "\n".join([ll.rstrip() for ll in all_textEmptyLines.splitlines() if ll.strip()])
    #subtracts useless text from useful text 
    useful_text = all_text.replace(deletable, "").replace(":","\n")

    #find the index where the phrase "Owner_Current" is in all_text. The line under it should be the actual account name.
    accountNameIndex = useful_text.find("Owner_Current")
    #using the index of the phrase "Owner_Current", removes everything before it in order to make the first line "Owner_Current"
    #and the second line the account name. This allows us to know what line number the information we want is on.
    accountNameAndTheRest = useful_text[accountNameIndex:]
    #makes the string a list of lines, takes the second line, removes all white space, and in the situations where there was an 
    #"&" in the account name, it changes the strange return value of it to a normal &. There are multiple things on this line
    #so using regex we find the first quoted value which is what we want
    accountName = re.findall('"([^"]*)"', accountNameAndTheRest.splitlines()[1].strip().replace("&amp","&"))[0]

    #the next lines do the same thing except with their respective fields
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
    
#when you run the program you say "python grabDataHalifax.py PRNs.txt". This sets script = grabDataHalifax.py and 
#filename = PRNs.txt.
script, filename = argv
#opens the list of parcel numbers
txt = open(filename).read()
#makes a list of parcel numbers out of the file inputted. Each line is a parcel and THE FIRST LINE IS IGNORED
PRNs = txt.split('\n')[1:]

#sets the file to write to as "Halifax County.csv"
filename = 'Halifax County.csv'
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


