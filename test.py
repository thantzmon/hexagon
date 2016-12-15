import urllib2
import json
response = urllib2.urlopen('https://www.webgis.net/va/halifax/')
html = response.read()
parsed = json.dumps(html) 
print(parsed)
