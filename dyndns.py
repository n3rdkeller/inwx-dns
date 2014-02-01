#!/usr/bin/env python2

# imports
import inwx
import os
from socket import getaddrinfo, gethostname, gethostbyname
from ConfigParser import ConfigParser
from time import strftime

# globals
api_url = "https://api.domrobot.com/xmlrpc/"
logfile = None
username = None
password = None
domain = None
subdomain = None
iptype = None
DATEANDTIME_FORMAT = "%d.%m.%y %H:%M:%S"
LOG_NEWLINE = "\n" + str((len(DATEANDTIME_FORMAT) + 3) * " ")

def log(logtext):
    if logfile != None:
        if not os.path.exists(logfile):
            print(dateandtime() + "Logfile doesn't exist. Creating: " + logfile)
        f = open(logfile, "a")
        f.write(dateandtime() + logtext + "\n")
        f.close()
    print(dateandtime() + logtext)

def dateandtime():
    return strftime("[" + DATEANDTIME_FORMAT + "] ")

def readconfig():
    try:
        cfg = ConfigParser()
        cfg.read("config.ini")
        global username, password, domain, subdomain, logfile
        username = cfg.get("General", "username")
        password = cfg.get("General", "password")
        domain = cfg.get("General", "domain")
        subdomain = cfg.get("General", "subdomain")
        iptype = int(cfg.get("General", "iptype"))
        try:
            logfile = cfg.get("General", "logfile")
            log("Now logging to " + logfile + ".")
        except:
            log("No logfile provided. Shell-logging only.")
            logfile = None
        return True
    except:
        log("Error reading your config.ini. Check and try again.")
        return False

def getip(iptype):
    try:
        if iptype == 4: # for ipv4 (only local)
            return gethostbyname(socket.gethostname())
        elif iptype == 6: # for ipv6 (maybe not working in all OS)
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
        if ninfo["record"][i]["name"] == (subdomain + "." + domain):
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
        log("IP changed from:" + LOG_NEWLINE + old + \
            LOG_NEWLINE + "to:" + LOG_NEWLINE + ip)
        try:
            conn.nameserver.updateRecord({"id": nid, "content": ip})
        except KeyError:
            pass
        except Exception, e:
            log("Error occured: " + e)
        log("Updated Nameserver-Record for " + subdomain + "." + domain)
    else:
        log("IP was not updated.")

if __name__ == "__main__":
    if readconfig():
        main()
    else:
        log("Exited without doing anything.")