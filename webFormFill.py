
#import django.http.request as requests
#import lxml.html as lh

import urllib
import urllib2
import webbrowser

url = 'http://duckduckgo.com/html'        # target url
data = urllib.urlencode({'q':'Python'})   # put string Python in field q
results = urllib2.urlopen(url,data)
with open('page.html', 'w') as pageFile:
    pageFile.write(results.read())

webbrowser.open('page.html')


# see stackoverflow 'using python to sign into website,
