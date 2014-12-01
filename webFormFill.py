
#import lxml.html as lh

import io
import urllib
import urllib2
import webbrowser

url = 'https://duckduckgo.com/html'       # target URL
data = urllib.urlencode({'q':'Python'})   # put string 'Python' in field 'q'
results = urllib2.urlopen(url, data)      # open URL with DATA, get html
with open('page.html', 'w') as pageFile:  # open the file to store html
    pageFile.write(results.read())        # write to file

webbrowser.open('page.html')              # view the html


# see stackoverflow 'using python to sign into website,
