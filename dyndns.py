#!/usr/bin/env python

# imports
import inwx
from ConfigParser import ConfigParser

# globals
api_url = "https://api.domrobot.com/xmlrpc/"
username = ""
password = ""
domain = ""

def readconfig():
    cfg = ConfigParser()
    cfg.read("config.ini")
    global username, password, domain
    username = cfg.get("General", "username")
    password = cfg.get("General", "password")
    domain = cfg.get("General", "domain")

def main():
    cred = {"lang": "en", "user": username, "pass": password}
    dom = {"domain": domain}
    conn = inwx.domrobot(api_url)
    login = conn.account.login(cred)
    check = conn.domain.check(dom)
    print(inwx.prettyprint.domain_check(check))

if __name__ == "__main__":
    readconfig()
    main()