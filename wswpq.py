# complete code that performs the scraping
# and prints a simple report to the standard output is:
""" Scrape packpub article network """
import mechanize
from BeautifulSoup import BeautifulSoup
import webbrowser  # for debug

def scrape_links(base_url, data):
    """ Scrape links pointing to article pages """
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
                #print str(anchor.string)
                #print str(anchor['href'])
                linkList.append(link)
    return linkList

def scrape_articles(data):
    """     Scrape the title and url of all the articles in this page """
    # URL prefix is used to filter out other links
    # such as the ones pointing to books
    articles = []
    ARTICLE_URL_PREFIX = '/books/content/'
    soup = BeautifulSoup(data)
    for li in soup.findAll('link'):
            for name, value in li.attrs:
                if str(name) == 'href':
                    if str(value).startswith(ARTICLE_URL_PREFIX):
                        articles.append( {'title': str(li.string),
                                            'url': str(li['href']) } )
                        print {'title': str(li.string),
                                 'url': str(li['href']) }
    return articles

def main():
    """
    Get article network main page and follow the links
    to get the whole list of articles available
    """
    articles = []

    # Get main page and get links to all article pages
    BASE_URL = "https://www.packtpub.com/books/content/article-network"
    ##BASE_URL = "https://www.packtpub.com/books/content/blogs"
    br = mechanize.Browser()
    data = br.open(BASE_URL).get_data()
    ## # save data as web page and view data in browser
    ##with open('page.html', 'w') as pageFile: # open the file to store html
    ##    pageFile.write(data)                 # write to file
    ##webbrowser.open_new_tab('page.html')     # view the html
    links = scrape_links(BASE_URL, data)

    # Scrape articles in main page
    articles.extend(scrape_articles(data))

    # Scrape articles in linked pages with relative links
    for link in links[1:]:
        if str(link.url).startswith('http'):
            pass
        else:
            print 'main: ' , link
            data = br.follow_link(link).get_data()
            articles = scrape_articles(data)
            articles.extend(articles)
            br.back()
            print 'main: ' , articles
    # Ouput is the list of titles and URLs for each article found
    print ("Article Network\n"
    "---------------")
    print "nn".join(['Title: "%(title)s"nURL: "%(url)s"' % article
                        for article in articles])

if __name__ == "__main__":
    main()
