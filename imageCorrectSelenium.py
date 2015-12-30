# code that requests does a violation search,
# corrects the plate and state information,
# saves the changes and moves to the next image
"""
Scrape packpub article network
"""
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0


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
    login to the SCIP portal
    """
    BASE_URL = "https://lprod.scip.ntta.org/portal/login"
    driver = webdriver.Ie()
    driver.get(BASE_URL);

    data = driver.get(BASE_URL)



if __name__ == "__main__":
    main()
