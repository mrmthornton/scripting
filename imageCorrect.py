# code that requests does a violation search,
# corrects the plate and state information,
# saves the changes and moves to the next image

from BeautifulSoup import BeautifulSoup
from windmill.authoring import WindmillTestClient
import windmill.browser
import re
import urlparse
from copy import copy


def get_massage():
    """
    Provide extra data massage to solve HTML problems in BeautifulSoup
    """
    # Javascript code in ths page generates HTML markup
    # that isn't parsed correctly by BeautifulSoup.
    # To avoid this problem, all document.write fragments are removed
    my_massage = copy(BeautifulSoup.MARKUP_MASSAGE)
    my_massage.append((re.compile(u"document.write(.+);"), lambda match: ""))
    my_massage.append((re.compile(u'alt=".+">'), lambda match: ">"))
    return my_massage

def main():
    """
    Scrape NASA Image of the Day Gallery
    """
    # Extra data massage for BeautifulSoup
    my_massage = get_massage()
    # Open main gallery page

    br = windmill.browser
    url = 'https://lprod.scip.ntta.org/portal/login'
    br.windmill.get_test_url(url)

    client = WindmillTestClient()
    print __name__
    client.open(url='https://lprod.scip.ntta.org/portal/login')
    # Page isn't completely loaded until image gallery data
    # has been updated by javascript code
    client.waits.forElement(xpath=u"//div[@id='gallery_image_area']/img", timeout=30000)
    # Scrape all images information
    images_info = {}
    while True:
        image_info = get_image_info(client, my_massage)
        # Break if image has been already scrapped
        # (that means that all images have been parsed
        # since they are ordered in a circular ring)
        if image_info['link'] in images_info:
            break
        images_info[image_info['link']] = image_info
        # Click to get the information for the next image
        client.click(xpath=u"//div[@class='btn_image_next']")
        # Print results to stdout ordered by image name
        for image_info in sorted(images_info.values(),
                       key=lambda image_info: image_info['name']):
            print ("Name: %(name)sn" "Link: %(link)sn" % image_info)


if __name__ == '__main__':
    main()

