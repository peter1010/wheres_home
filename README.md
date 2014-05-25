track_my_ip
===========

This package is run as a service that finds out your public IP address
and then emails it to a specificed email account. The objective
is to know your home IP address when you are away allowing you to 
connect home (assuming you have allowed access e.g. via enabling
port forwarding on your router).

This is an alternative to using a DDNS service.

details
-------

This is a python package that is called from a systemd timer and
uses the STUN protocol to ask a STUN server what your IP address
is. The IP address is stored in a file so each time the package is
run it can check if it has changed. If the IP address has changed
an email is sent to the specificed email address and the subject
contains the new IP address.

dependencies
------------

This package depends on:

- systemd timers
- sendmail or sendmail alternative like msmtp-mta

IP address is recorded in /var/cache/track_my_ip/history.txt
Email address is read from /etc/track_my_ip/email

installation
------------

There is a PKGBUILD for those that use pacman, makepkg will build a package.

Alternative ./setup.py install will install using the python distutils.
