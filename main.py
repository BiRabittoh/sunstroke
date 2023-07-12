import json
import requests # https://github.com/pyload/pyload/wiki/module.Api.Api
from Sole import get_sole, remove_first

SESSION_FILENAME = "session.txt"
PYLOAD_PROTOCOL = "http"
PYLOAD_HOST = "localhost"
PYLOAD_PORT = 8000
PYLOAD_USER = "pyload"
PYLOAD_PW = "pyload"
PYLOAD_API_ENDPOINT = "/api"
PYLOAD_LOGIN_ENDPOINT = "/login"
PYLOAD_ADDPACKAGE_ENDPOINT = "/generateAndAddPackages"
PYLOAD_API_URL = f"{ PYLOAD_PROTOCOL }://{ PYLOAD_HOST }:{ PYLOAD_PORT }{ PYLOAD_API_ENDPOINT }"

LOGIN_DATA = { "username": PYLOAD_USER, "password": PYLOAD_PW }
LOGIN_URL = PYLOAD_API_URL + PYLOAD_LOGIN_ENDPOINT
ADDPACKAGE_URL = PYLOAD_API_URL + PYLOAD_ADDPACKAGE_ENDPOINT

def get_session_id():
    try:
        with open(SESSION_FILENAME, "r", encoding="utf-8") as in_file:
            return in_file.readline()
    except FileNotFoundError:
        res = requests.post(LOGIN_URL, data=LOGIN_DATA)
        cookies = res.cookies.get_dict()
        session_id = cookies['pyload_session']
        with open(SESSION_FILENAME, "w", encoding="utf-8") as out_file:
            out_file.write(session_id)
        return session_id
    
def add_package(links):
    ADDPACKAGE_DATA = { "links": json.dumps(links), "session": session_id }
    print(ADDPACKAGE_URL)
    print(ADDPACKAGE_DATA)
    kek = requests.post(ADDPACKAGE_URL, data=LOGIN_DATA).text
    return kek

if __name__ == "__main__":
    session_id = get_session_id()
    
    #sole = get_sole()
    #sole_link = remove_first(sole)[1][0]
    
    
    links = [ "http://localhost:8080/file2", "http://localhost:8080/file1" ]
    
    print(add_package(links))
