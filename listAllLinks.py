#-------------------------------------------------------------------------------
# Name:        get_next_target
# Purpose:
#
# Author:      IEUser
#
# Created:     16/11/2014
# Copyright:   (c) IEUser 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def fix_machine(debris, product):
    i = 0
    out = ""
    while i < len(product):
        pos = debris.find(product[i])
        if pos == -1:
            return "Give me something that's not useless next time."
        out = out + debris[pos]
        i = i + 1

    return out

def bigger(a,b):
    if a > b:
        return a
    else:
        return b

def biggest(a,b,c):
    return bigger(a,bigger(b,c))

def median(a, b, c):
    first = biggest(a, b, c)
    if a == first:
        return bigger(b,c)
    if b == first:
        return bigger(a,c)
    if c == first:
        return bigger(a,b)

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"' , start_link)
    end_quote = page.find('"' , start_quote + 1)
    url = page[start_quote + 1 : end_quote]
    return url, end_quote

def getAllLinks(page):
    urlList =[]                            # start with an empty list
    while True:
        url, start_next = get_next_target(page)  # look for next link
        if url:
            urlList.append(url)         # if there is a next, save it,
            page = page[start_next:]    # and shring the page string
        else:
            break                       # no more links on this page
    return urlList

def crawlWeb(seed):
    toCrawl = [seed]
    crawled = []
    while toCrawl:
        page = toCrawl.pop()
        if page not in crawled:
            for link in getAllLinks(page):
                toCrawl.append(link)
    return crawled


def main():
    page =('<div id="top_bin"><div id="top_content" class="width960">'
    '<div class="udacity float-left"><a href="http://udacity.com">')
    #page = get_page('http://xkcd.com/353')
    #page = get_page('http://www.udacity.com/cs101x/index.html')
    listOfLinks = getAllLinks(page)
    print listOfLinks

if __name__ == '__main__':
    main()


