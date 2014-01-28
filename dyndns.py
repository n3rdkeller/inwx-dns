#!/usr/bin/env python

# imports
import inwx
from ConfigParser import ConfigParser

# globals
api_url = "https://api.domrobot.com/xmlrpc/"
username = ""
password = ""
domain = ""
cred = {"lang": "en", "user": username, "pass": password}
dom = {"domain": domain}

def main():
    # global cred, dom, username, password, domain, api_url
    conn = inwx.domrobot(api_url, False)
    login = conn.account.login(cred)
    check = conn.domain.check(dom)
    print(inwx.prettyprint.domain_check(check))
    
if __name__ == "__main__":
    main()