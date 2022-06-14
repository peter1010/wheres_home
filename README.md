wheres_home
===========

This package is run as a service that finds out your public IP address
and logs to a history file.

details
-------

This is a python package that needs to be called from a timer and
uses the STUN protocol to ask a STUN server what your IP address
is. The IP address is stored in a file so each time the package is
run it can check if it has changed.

dependencies
------------

This package depends on:

- systemd timers
- sendmail or sendmail alternative like msmtp-mta

IP address is recorded in stub_history.txt in current working directory

installation
------------

Alternative ./setup.py install will install using the python distutils.
