#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      IEUser
#
# Created:     16/11/2014
# Copyright:   (c) IEUser 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------


# Write Python code that assigns to the
# variable url a string that is the value
# of the first URL that appears in a link
# tag in the string page.
# Your code should print http://udacity.com
# Make sure that if page were changed to
# page = '<a href="http://udacity.com">Hello world</a>'
# that your code still prints the same thing.

# page = contents of a web page
page =('<div id="top_bin"><div id="top_content" class="width960">'
'<div class="udacity float-left"><a href="http://udacity.com">')
start_link = page.find('<a href=')
start_quote = page.find('"' , start_link)
end_quote = page.find('"' , start_quote + 1)
url = page[start_quote + 1 : end_quote]

print url
