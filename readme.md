# inwx-dns
This tool is to update the nameserver entry of our domain to the IPv6-address of our homeserver.

It uses the [XML-API](http://www.inwx.de/de/offer/api) of our registrar [InterNetworX](http://inwx.de/).
They also build the library we used (`inwx.py`).



## Config-File
You will need a config-file `config.ini` for this script to work. It's ignored by git because the credentials are in there unencrypted. Create the file with the following syntax in the repository-folder:

    [General]
    username=root
    password=unsafepass
    domain=xyz.com

