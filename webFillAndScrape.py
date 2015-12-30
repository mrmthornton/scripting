
#import django.http.request as requests
#import lxml.html as lh

import io
import re
import urllib
import urllib2
import webbrowser
<<<<<<< HEAD
#import jsScrape

from lxml import html

url = 'http://www.txdps.state.tx.us/search/searchresults.asp'
data = urllib.urlencode({'q':'TRS'})   # html form of 'field' gets 'value'
##url = 'https://duckduckgo.com/html'       # target URL
##data = urllib.urlencode({'q':'Python'})   # html form of 'q gets value Python'
##url = 'https://accounts.google.com/ServiceLoginAuth'       # target URL
##data = urllib.urlencode({'Email':'mrmthornton@gmail.com', 'Passwd':'randomGmail'})
##data = urllib.urlencode({'Email':'mrmthornton@gmail.com'})

##request = urllib2.Request(url)            # formulate a request
request = urllib2.Request(url, data)      # formulate a request
opener = urllib2.build_opener()
opener.addheaders = [('User-Agent','Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)')]
##results = urllib2.urlopen(request)      # open URL with DATA, get html
results = opener.open(request)      # open URL with DATA, get html
content = results.read()               # get string version of page

print request
print type(request)
print results
print type(results)
# get the javasript produced HTML
##wkdl = jsScrape.WebkitDownloader()
##wkdl.process_request(request, '')


=======
from lxml import html

url = 'https://lprod.scip.ntta.org/portal/login'
data = urllib.urlencode({'q':'Python'})   # html form of 'q gets value Python'
##url = 'https://lsso.rite.ntta.org/px/lg_vps_prod/vpvios03$vio.actionquery'
##url = 'https://prod1.dot.state.tx.us/'
##data = urllib.urlencode({'q':'overridelink'})   # html form of 'q gets value Python'

#url = 'https://mvdinet.txdmv.gov/cics/mvinq/menu.html' #404 unauth
#url = 'https://mvdinet.txdmv.gov/cics/mvinq/regs.html' #404 unauth

#url = 'https://simple.wikipedia.org/wiki/Main_Page'

#url = 'https://duckduckgo.com/html'       # target URL
#data = urllib.urlencode({'q':'Python'})   # html form of 'q gets value Python'



request = urllib2.Request(url)
#request = urllib2.Request(url, data)      # formulate a request
results = urllib2.urlopen(request)        # open URL with DATA, get html
content = results.read()                  # get string version of page
>>>>>>> c4a95a9e05e29d475bb078e903c178926551f7b2
# save content as web page
with open('page.html', 'w') as pageFile:  # open the file to store html
    pageFile.write(content)               # write to file
# view content in browser
<<<<<<< HEAD
webbrowser.open_new_tab('page.html')      # view the html

# extract text portion of page
snippetStartPattern = re.compile('title="Welcome!">')
foundStart = snippetStartPattern.search(content)
if foundStart != None:
    content = content[foundStart.end():]
    snippetEndPattern = re.compile('</div>')
    foundEnd = snippetEndPattern.search(content)
    if foundEnd != None:
        content = content[:foundEnd.start()]
        print content

##            snippet = content[:foundEnd.start() + 1]
##            snippet.replace('<b>', '')
##            print snippet
##            content = content[foundEnd.end():]
##    else:
##        break
=======
webbrowser.open('page.html')              # view the html

# extract text portion of page
##snippetStartPattern = re.compile('title="Welcome!">')
##foundStart = snippetStartPattern.search(content)
##if foundStart != None:
##    content = content[foundStart.end():]
##    snippetEndPattern = re.compile('</div>')
##    foundEnd = snippetEndPattern.search(content)
##    if foundEnd != None:
##        content = content[:foundEnd.start()]
##        print content

#            snippet = content[:foundEnd.start() + 1]
#            snippet.replace('<b>', '')
#            print snippet
#            content = content[foundEnd.end():]
#    else:
#        break
>>>>>>> c4a95a9e05e29d475bb078e903c178926551f7b2


# see stackoverflow 'using python to sign into website,
