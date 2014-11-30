#
# This question explores a different way (from the previous question)
# to limit the pages that it can crawl.
#
#######

# THREE GOLD STARS #
# Yes, we really mean it!  This is really tough (but doable) unless
# you have some previous experience before this course.


# Modify the crawl_web procedure to take a second parameter,
# max_depth, that limits the depth of the search.  We can
# define the depth of a page as the number of links that must
# be followed to reach that page starting from the seed page,
# that is, the length of the shortest path from the seed to
# the page.  No pages whose depth exceeds max_depth should be
# included in the crawl.
#
# For example, if max_depth is 0, the only page that should
# be crawled is the seed page. If max_depth is 1, the pages
# that should be crawled are the seed page and every page that
# it links to directly. If max_depth is 2, the crawl should
# also include all pages that are linked to by these pages.
#
# Note that the pages in the crawl may be in any order.
#
# The following definition of get_page provides an interface
# to the website found at http://www.udacity.com/cs101x/index.html

# The function output order does not affect grading.
import re


def get_page(url):
    try:
        import urllib
        #import urllib2
        #import urlparse
        return urllib.urlopen(url).read()
    except:
        return ""

def add_to_index(index,keyword,url):
    length = len(index)
    for idx in index:
        if idx[0] == keyword:
            if url not in idx[1]:
                idx[1].append(url)
            return
    index.append([keyword,[url]])

def add_page_to_index(index,url,content):
    wordlist = content.split()
    for word in wordlist:
        add_to_index(index, word, url)

def lookup(index,keyword):
    for idx in index:
        if idx[0] == keyword:
            return idx[1]
    return []

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def crawl_web(seed,max_depth):
    depth = 0
    tocrawl = [seed]
    crawled = []
    next_depth = []
    index = []
    while tocrawl and depth <= max_depth:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index,page,content)
            union(next_depth, get_all_links(get_page(content)))
            crawled.append(page)
        if not tocrawl:
            tocrawl, next_depth = next_depth, []
            depth = depth + 1
    return index

#anIndex = crawl_web("http://www.udacity.com/cs101x/index.html",0)
#for e in anIndex:
#    print e

#anIndex = crawl_web("http://www.udacity.com/cs101x/index.html",1)
#for e in anIndex:
#    print e

#anIndex = crawl_web("http://www.udacity.com/cs101x/index.html",50)
#for e in anIndex:
#    print e

anIndex = crawl_web("http://www.ntta.org",0)
for e in anIndex:
    print e

