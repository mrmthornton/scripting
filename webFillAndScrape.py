
#import django.http.request as requests
#import lxml.html as lh

import io
import re
import urllib
import urllib2
import webbrowser
from lxml import html

#url = 'https://duckduckgo.com/html'       # target URL
#data = urllib.urlencode({'q':'Python'})   # html form of 'q gets value Python'
url = 'https://accounts.google.com/ServiceLoginAuth'       # target URL
data = urllib.urlencode({'Email':'mrmthornton@gmail.com', 'Passwd':'randomGmail'})
request = urllib2.Request(url, data)      # formulate a request
results = urllib2.urlopen(request)        # open URL with DATA, get html
content = results.read()                  # get string version of page
#print content

with open('page.html', 'w') as pageFile:  # open the file to store html
    pageFile.write(content)               # write to file

webbrowser.open('page.html')              # view the html

snippet = ''

while True:
    snippetStartPattern = re.compile('<div class="snippet">')
    foundStart = snippetStartPattern.search(content)
    if foundStart != None:
        content = content[foundStart.end():]
        snippetEndPattern = re.compile('</div>')
        foundEnd = snippetEndPattern.search(content)
        if foundEnd != None:
            snippet = content[:foundEnd.start() + 1]
            snippet.replace('<b>', '')
            print snippet
            content = content[foundEnd.end():]
    else:
        break


# see stackoverflow 'using python to sign into website,