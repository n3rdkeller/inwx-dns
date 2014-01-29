#!/usr/bin/env python2

# imports
import inwx
from socket import getaddrinfo, gethostname, gethostbyname
from ConfigParser import ConfigParser

# globals
api_url = "https://api.domrobot.com/xmlrpc/"
username = None
password = None
domain = None
subdomain = None
iptype = None

def readconfig():
    try:
        cfg = ConfigParser()
        cfg.read("config.ini")
        global username, password, domain, subdomain
        username = cfg.get("General", "username")
        password = cfg.get("General", "password")
        domain = cfg.get("General", "domain")
        subdomain = cfg.get("General", "subdomain")
        iptype = int(cfg.get("General", "iptype"))
    except:
        print("Error reading your config.ini. Check and try again.")

def getip(type: int):
    try:
        if type == 4: # for ipv4
            return gethostbyname(socket.gethostname())
        elif type == 6: # for ipv6 (maybe not working in all OS)
            return getaddrinfo(gethostname(), None)[0][4][0]
    except:
        return None

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

    global iptype
    ip = getip(iptype)
    if (ip != None) and (ip != old):
        # update the record
        print("IP changed from:\n" + old + "\nto:\n" + ip)
        try:
            conn.nameserver.updateRecord({"id": nid, "content": ip})
        except KeyError:
            pass
        print("Updated Nameserver-Record for server." + domain)

if __name__ == "__main__":
    readconfig()
    main()