import feedparser
from html.parser import HTMLParser
from datetime import datetime
from re import compile

N_LINKS_TO_REMOVE = 2
REGEX_DATE = compile("\(([\d\.]*)\)")
OVERPOST_URL = "https://overpost.biz/e-books/quotidiani/rss.xml"

def add_or_update(dictionary, key, value):
    try:
        dictionary[key].append(value)
    except KeyError:
        dictionary[key] = [ value ]

class PostParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = {}
        self.prev_tag = None
        self.current_tag = None
        self.current_link = None
    
    def handle_starttag(self, tag, attrs):
        if tag == "br":
            return
        self.prev_tag = self.current_tag
        self.current_tag = tag
        if tag == "a":
            for at in attrs:
                if at[0] == "href":
                    self.current_link = at[1]

    def handle_endtag(self, tag):
        self.current_tag = self.prev_tag

    def handle_data(self, data):
        if self.current_tag == "a":
            key = data.replace("_", " ").split(" - ")[0]
            value = self.current_link
            add_or_update(self.links, key, value)
            
    def get_links(self):
        return self.links.copy()
    
def parse_html(html):
    parser = PostParser()
    parser.feed(html)
    return parser.get_links()

def remove_first(d):
    return (k := next(iter(d)), d.pop(k))

def remove_first_n(d, n):
    for i in range(n):
        remove_first(d)

def parse_entry(entry): # entry = day
    date = REGEX_DATE.findall(entry.title)[0]
    links = parse_html(entry.turbo_content)
    
    remove_first_n(links, N_LINKS_TO_REMOVE)
    return (datetime.strptime(date, "%d.%m.%Y"), links)

def get_links(rss_url):
    feed = feedparser.parse(rss_url)
    return [ parse_entry(entry) for entry in feed.entries ]

def get_sole():
    links = get_links(OVERPOST_URL)
    today = links[1]
    return { k: v for k, v in today[1].items() if k.startswith("Il Sole 24 Ore")}

OVERPOST_URL = r"/home/marco/Documenti/overpost/rss.xml"
if __name__ == "__main__":
    print(get_sole())
