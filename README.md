track_my_ip
===========

Bunch of python scripts to sort of replicate the behaviour of
DDNS. A periodic task that uses STUN to find out the public
IP Address and if it changes records the new value in a way
that it can be picked up remotely. This aids connecting
home from a remote location.

The record changes can be configured to:
- email the new IP address.
- use dropbox.
- use API of a DDNS provider.

In additional the change of IP address is logged locally
so we can track how the ISP allocates IP addresses to us.
