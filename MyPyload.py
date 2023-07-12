# My edited version of https://github.com/thammi/pyload-utils/blob/master/pyloadutils/pyload.py
import json
from urllib.request import urlopen
from urllib.parse import urljoin, urlencode
from dotenv import load_dotenv
from os import getenv
load_dotenv()

PYLOAD_HOST = getenv("PYLOAD_HOST") or "http://localhost:8000/"
PYLOAD_USER = getenv("PYLOAD_USER") or "pyload"
PYLOAD_PW = getenv("PYLOAD_PW") or "pyload"

class Pyload:

    def __init__(self):
        self.url_base = urljoin(PYLOAD_HOST, 'api/')
        self.session = self._call('login', {'username': PYLOAD_USER, 'password': PYLOAD_PW}, False)

    def _call(self, name, args={}, encode=True):
        url = urljoin(self.url_base, name)

        if encode:
            data = { k: json.dumps(v) for k, v in args.items() }
        else:
            data = args

        if hasattr(self, 'session'):
            data['session'] = self.session

        post = urlencode(data).encode('utf-8')
        return json.loads(urlopen(url, post).read().decode('utf-8'))

    def __getattr__(self, name):
        def wrapper(**kargs):
            return self._call(name, kargs)
        return wrapper
