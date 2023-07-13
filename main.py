
from urllib.error import URLError
from datetime import datetime
from os import getenv
from dotenv import load_dotenv
load_dotenv()
from Overpost import get_newspaper
from MyPyload import Pyload

NEWSPAPER_PREFIX = getenv("NEWSPAPER_PREFIX") or ""
HOST_PREFERENCE = [ 'katfile.com', 'rapidgator.net', 'www.easybytez.com' ]

def scroll_list(array, buffer=1000):
    array_len = len(array)
    i = 0
    while i < buffer:
        if i >= array_len:
            i = 0
        yield array[i]
        i += 1

def get_host(link):
    return link.split("/")[2]

def filter_links(links, hosts):
    host = next(hosts)
    for link in links:
        print(link, host)
        if get_host(link) == host:
            return link
    return filter_links(links, hosts)
        
        
def get_sorted_links(dictionary):
    hosts = scroll_list(HOST_PREFERENCE)
    return [ filter_links(links, hosts) for _, links in dictionary.items() ]

def download_link(connection, name, link):
    return connection.addPackage(name=name, links=[link])

def handle_links(name, links):
    try:
        con = Pyload()
        return [ download_link(con, name, link) for link in links ]
    except URLError:
        print("\nConnessione a Pyload rifiutata.")

    print(len(links), "link da aggiungere manualmente:\n")
    for link in links:
        print(link)
    print()
    return []

def main():
    newspapers = get_newspaper(NEWSPAPER_PREFIX, 0) # 0 -> today
    name = f"{NEWSPAPER_PREFIX} - {datetime.today().strftime('%Y-%m-%d')}"
    links = get_sorted_links(newspapers)
    pids = handle_links(name, links)
    print(len(pids), "link aggiunti a Pyload.")
    print("Premi INVIO per uscire.")
    input()

if __name__ == "__main__":
    exit(main())
