from html.parser import HTMLParser
from datetime import datetime
from re import compile
import os
import feedparser
from MyResolver import get

RSS_URL = os.getenv("RSS_URL") or os.path.join(".", "rss.xml")
N_LINKS_TO_REMOVE = os.getenv("N_LINKS_TO_REMOVE") or 2
REGEX_DATE = compile("\(([\d\.]*)\)")

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

def dict_pop(d):
    return (k := next(iter(d)), d.pop(k))

def dict_pop_first_n(d, n):
    return [dict_pop(d) for _ in range(n)]

def parse_entry(entry): # entry = day
    date = REGEX_DATE.findall(entry.title)[0]
    links = parse_html(entry.turbo_content)
    
    dict_pop_first_n(links, int(N_LINKS_TO_REMOVE))
    return (datetime.strptime(date, "%d.%m.%Y"), links)

def handle_url(url):
    if url.startswith("http"):
        return get(url).text
    else:
        return url

def get_links(rss_url):
    feed = feedparser.parse(handle_url(rss_url))
    return [ parse_entry(entry) for entry in feed.entries ]

def get_newspaper(prefix="", index=0):
    all_links = get_links(RSS_URL)
    try:
        daily = all_links[index][1]
    except IndexError:
        print("Empty feed.")
        return {}
    return { k: v for k, v in daily.items() if k.startswith(prefix)}

if __name__ == "__main__":
    print(get_newspaper("Il Sole"))
