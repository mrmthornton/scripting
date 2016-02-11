# complete code that performs the scraping
# and prints a simple report to the standard output is:
"""
Scrape packpub article network
"""
import mechanize
from BeautifulSoup import BeautifulSoup
import webbrowser  # for debug

def scrape_links(base_url, data):
    """
    Scrape links pointing to article pages
    """
    soup = BeautifulSoup(data)

    # Create mechanize links to be used
    # later by mechanize.Browser instance
    linkList = []
    for anchor in soup.findAll("a"):
        for name, value in anchor.attrs:
            if str(name) == 'href':
                link = mechanize.Link(  base_url = base_url,
                                        url = str(anchor['href']),
                                        text = str(anchor.string),
                                        tag = str(anchor.name),
                                        attrs = [(str(name), str(value))])
                print str(anchor.string)
                print str(anchor['href'])
                linkList.append(link)
    return linkList
##    links = [
##            mechanize.Link(base_url = base_url,
##                            url = str(anchor['href']),
##                            text = str(anchor.string),
##                            tag = str(anchor.name),
##                            attrs = [(str(name), str(value))
##                                for name, value in anchor.attrs])
                # in the original code the method 'soup.right.findAll() does not exist?
                #for anchor in soup.right.findAll("a")]
##                for anchor in soup.findAll('href')
##            ]
##    return links

def scrape_articles(data):
    """
    Scrape the title and url of all the articles in this page
    """
    # URL prefix is used to filter out other links
    # such as the ones pointing to books
    articles = []
    ARTICLE_URL_PREFIX = 'http://www.packtpub.com/article/'
    soup = BeautifulSoup(data)
    for anchor in [li.a for li in soup.findAll('li')]:
        if anchor != None:
            for name, value in anchor.attrs:
                if str(value).startswith(ARTICLE_URL_PREFIX):
                    articles.append( {'title': str(anchor.string),
                                        'url': str(anchor['href']) } )
                    print {'title': str(anchor.string),
                                        'url': str(anchor['href']) }
    return articles

def main():
    """
    Get article network main page and follow the links
    to get the whole list of articles available
    """
    articles = []

    # Get main page and get links to all article pages
    BASE_URL = "http://www.packtpub.com/article-network"
    br = mechanize.Browser()
    data = br.open(BASE_URL).get_data()

    # save data as web page             #### for debug
    ##with open('page.html', 'w') as pageFile:  # open the file to store html
    ##    pageFile.write(data)               # write to file
    # view data in browser
    ##webbrowser.open_new_tab('page.html')      # view the html

    links = scrape_links(BASE_URL, data)

    # Scrape articles in main page
    articles.extend(scrape_articles(data))

    # Scrape articles in linked pages
    ##for link in links[1:]:
    ##    data = br.follow_link(link).get_data()
    ##    articles.extend(scrape_articles(data))
    ##    br.back()

    # Ouput is the list of titles and URLs for each article found
    print ("Article Network\n"
    "---------------")
    print "nn".join(['Title: "%(title)s"nURL: "%(url)s"' % article
                        for article in articles])

if __name__ == "__main__":
    main()