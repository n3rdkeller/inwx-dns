#!/usr/bin/env python

# imports
import inwx
from socket import getaddrinfo, gethostname
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

def getip():
    return (getaddrinfo(gethostname(), None)[0][4][0])

def main():
    # login credentials
    cred = {"lang": "en", "user": username, "pass": password}
    # domain for request
    dom = {"domain": domain}
    # domrobot object (for request)
    conn = inwx.domrobot(api_url)
    # login
    login = conn.account.login(cred)
    # get nameserver entries
    ninfo = conn.nameserver.info(dom)
    ncount = 0
    # get the one with "server."
    for i in range(len(ninfo["record"])):
        if ninfo["record"][i]["name"] == ("server." + domain):
            ncount = i
            break
    # save the id of the entry
    nid = ninfo["record"][ncount]["id"]

    # TODO
    # update the record

if __name__ == "__main__":
    readconfig()
    getip()
    main()