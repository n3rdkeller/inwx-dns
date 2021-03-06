# inwx-dns
This tool was originally made only to update the nameserver record of our domain to the local IP of our homeserver (Dynamic DNS Service). But due to the wish of some friends we updated it to fit more general purposes (but still only with our registrar).

It uses the [XML-API](http://www.inwx.de/de/offer/api) of our registrar [InterNetworX](http://inwx.de/).
They also build the library we used (`inwx.py`).

##### Just make sure the nameserver entry already exists before starting the script.
##### Also make sure the configured IP-type fits your record type (`A` or `AAAA`).

##### Attention! This script changes your DNS entries. Make really sure you really want this.
If not, you can change the API-URL in the script to `https://api.ote.domrobot.com/xmlrpc/`. This is the [OT&E](http://ote.inwx.de) API that can be used testing purposes. We only tested `inwx-dns` with the normal API, but it should be the same here.

To fetch your global IPv4, we use `http://ipecho.net/plain`. If you don't trust these guys, change this URL in the script to your own service-URL.



## Config-File
You will need a config-file `config.ini` for this script to work. It's ignored by git, because the credentials in this file are not encrypted. Create the file with the following syntax in the repository-folder:

    [General]
    username=root
    password=unsafepass
    domain=xyz.com
    subdomain=abc
    iptype=6             # can be 4 or 6
    #logfile=dyndns.log  # optional, uncomment if you want a logfile


## Issues
If you get into troubles, just open an issue and we will take a look into it.


## Todo

* Multi-Update (more than one entry)
* Update both at the same time, IPv4 and IPv6
* Support for more than one entry with this subdomain
* Rewrite their library

## Credits
Thanks to the guys of `ipecho.net` who provide an easy-to-use interface to fetch the global IPv4 address.