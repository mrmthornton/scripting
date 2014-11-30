#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      IEUser
#
# Created:     21/11/2014
# Copyright:   (c) IEUser 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#import django.http.request as requests
#import lxml.html as lh

import urllib
import urllib2

urllib.urlretrieve("http://github.com/login/", "somefile.html", lambda x,y,z:0, urllib.urlencode({"username": "mrmthornton", "password": "Publix5418Git"}))
hold = '''
gh_url = 'https://api.github.com'

req = urllib2.Request(gh_url)

password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
password_manager.add_password(None, gh_url, ' mrmthornton', 'Publix5418Git')

auth_manager = urllib2.HTTPBasicAuthHandler(password_manager)
opener = urllib2.build_opener(auth_manager)
urllib2.install_opener(opener)
handler = urllib2.urlopen(req)

print handler.getcode()
print handler.headers.getheader('content-type')
'''

# see stackoverflow 'using python to sign into website,
# fill in a form, then sign out

