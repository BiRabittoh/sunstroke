# My edited version of https://github.com/thammi/pyload-utils/blob/master/pyloadutils/pyload.py
import json
import requests
from urllib.parse import urljoin, urlencode, quote_plus
from dotenv import load_dotenv
from os import getenv
load_dotenv()

PYLOAD_HOST = getenv("PYLOAD_HOST") or "http://localhost:8000/"
PYLOAD_USER = getenv("PYLOAD_USER") or "pyload"
PYLOAD_PW = getenv("PYLOAD_PW") or "pyload"

PYLOAD_API_URL = PYLOAD_HOST + 'api/'
PYLOAD_LOGIN_URL = urljoin(PYLOAD_API_URL, 'login')
PYLOAD_ADDPACKAGE_URL = urljoin(PYLOAD_API_URL, 'add_package')

QUOTES = '"{}"'

class Pyload:

    def __init__(self):
        login_data = {'username': PYLOAD_USER, 'password': PYLOAD_PW}
        self.session = requests.Session()
        self.session.post(PYLOAD_LOGIN_URL, data=login_data)

    def addPackage(self, name: str, links: list, password: str = "", ):
        #link_string = [quote_plus(x) for x in links]
        name_string = QUOTES.format(name)
        link_string = json.dumps(links)

        request_data = { 'name': name_string, 'links': link_string }
        return self.session.post(url=PYLOAD_ADDPACKAGE_URL, data=request_data)
