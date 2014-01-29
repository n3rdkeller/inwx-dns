#!/usr/bin/env python2

# imports
import inwx
from socket import getaddrinfo, gethostname
from ConfigParser import ConfigParser

# globals
api_url = "https://api.domrobot.com/xmlrpc/"
username = None
password = None
domain = None
localv6 = None

def readconfig():
    cfg = ConfigParser()
    cfg.read("config.ini")
    global username, password, domain
    username = cfg.get("General", "username")
    password = cfg.get("General", "password")
    domain = cfg.get("General", "domain")

def getip():
    try:
        global localv6
        localv6 = getaddrinfo(gethostname(), None)[0][4][0]
    except:
        pass

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
    # get content of the old entry
    old = ninfo["record"][ncount]["content"]

    global localv6
    if (localv6 != None) and (localv6 != old):
        # update the record
        print("IP changed from:\n" + old + "\nto:\n" + localv6)
        try:
            conn.nameserver.updateRecord({"id": nid, "content": localv6})
        except KeyError:
            pass
        print("Updated Nameserver-Record for server." + domain)

if __name__ == "__main__":
    readconfig()
    getip()
    main()