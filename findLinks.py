#-------------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      IEUser
#
# Created:     16/11/2014
# Copyright:   (c) IEUser 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def get_page(url):
    try:
        if url == "http://www.udacity.com/cs101x/index.html":
            return ('<html> <body> This is a test page for learning to crawl! '
            '<p> It is a good idea to '
            '<a href="http://www.udacity.com/cs101x/crawling.html">learn to '
            'crawl</a> before you try to  '
            '<a href="http://www.udacity.com/cs101x/walking.html">walk</a> '
            'or  <a href="http://www.udacity.com/cs101x/flying.html">fly</a>. '
            '</p> </body> </html> ')
        elif url == "http://www.udacity.com/cs101x/crawling.html":
            return ('<html> <body> I have not learned to crawl yet, but I '
            'am quite good at '
            '<a href="http://www.udacity.com/cs101x/kicking.html">kicking</a>.'
            '</body> </html>')
        elif url == "http://www.udacity.com/cs101x/walking.html":
            return ('<html> <body> I cant get enough '
            '<a href="http://www.udacity.com/cs101x/index.html">crawling</a>! '
            '</body> </html>')
        elif url == "http://www.udacity.com/cs101x/flying.html":
            return ('<html> <body> The magic words are Squeamish Ossifrage! '
            '</body> </html>')
    except:
        return ""
    return ""


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

def union(base, addon):
    for e in addon:
        if e not in base:
            base.append(e)

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"' , start_link)
    end_quote = page.find('"' , start_quote + 1)
    url = page[start_quote + 1 : end_quote]
    return url, end_quote

def getAllLinks(page):
    links =[]
    while True:
        url, start_next = get_next_target(page)
        if url:
            links.append(url)
            page = page[start_next:]
        else:
            break
    return links

def crawlWeb(seed, maxPages):
    toCrawl = [seed]
    crawled = []
    while toCrawl:
        page = toCrawl.pop()
        if page not in crawled and len(crawled) < maxPages:
            crawled.append(page)
            union(toCrawl, getAllLinks(get_page(page))) # need get_page
    return crawled

def main():
    print crawlWeb("http://www.udacity.com/cs101x/index.html",1)
    print crawlWeb("http://www.udacity.com/cs101x/index.html",3)
    print crawlWeb("http://www.udacity.com/cs101x/index.html",500)

if __name__ == '__main__':
    main()



