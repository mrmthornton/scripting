# Define a procedure, add_to_index,
# that takes 3 inputs:

# - an index: [[<keyword>,[<url>,...]],...]
# - a keyword: String
# - a url: String

# If the keyword is already
# in the index, add the url
# to the list of urls associated
# with that keyword.

# If the keyword is not in the index,
# add an entry to the index: [keyword,[url]]

index = []

def add_to_index(index,keyword,url):
    length = len(index)
    for idx in index:
        if idx[0] == keyword:
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

print lookup(index, 'test')
#>>> []
add_to_index(index,'udacity','http://udacity.com')
add_to_index(index,'computing','http://acm.org')
add_to_index(index,'udacity','http://npr.org')
print index
#>>> [['udacity', ['http://udacity.com', 'http://npr.org']],
#>>> ['computing', ['http://acm.org']]]
print lookup(index,'udacity')
#>>> ['http://udacity.com','http://npr.org']
print lookup(index, 'test')
#>>> []