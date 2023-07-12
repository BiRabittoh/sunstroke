from Overpost import get_newspaper
from MyPyload import Pyload
from os import getenv

NEWSPAPER_PREFIX = getenv("NEWSPAPER_PREFIX") or ""

def scroll_dict(dictionary):
    i = 0
    for key, values in dictionary.items():
        if i >= len(values):
            i = 0
        yield key, values[i]
        i += 1

def download_link(connection, name, link):
    return connection.addPackage(name=name, links=[link])

def main():
    newspapers = get_newspaper(NEWSPAPER_PREFIX, 0) # 0 -> today
    con = Pyload()
    pids = [ download_link(con, NEWSPAPER_PREFIX, link) for _, link in scroll_dict(newspapers) ]
    print(pids)

if __name__ == "__main__":
    exit(main())
