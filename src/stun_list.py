import random
import socket
import logging

logger = logging.getLogger(__name__)

stun_servers_list = (
    "stun.l.google.com:19302",
    "stun1.l.google.com:19302",
    "stun2.l.google.com:19302",
    "stun3.l.google.com:19302",
    "stun4.l.google.com:19302",
    "stun01.sipphone.com",
    "stun.ekiga.net",
    "stun.fwdnet.net",
    "stun.ideasip.com",
    "stun.iptel.org",
    "stun.rixtelecom.se",
    "stun.schlund.de",
    "stunserver.org",
    "stun.softjoys.com",
    "stun.voiparound.com",
    "stun.voipbuster.com",
    "stun.voipstunt.com",
    "stun.voxgratia.org",
    "stun.xten.com"
)


def pick_server_name():
    """Pick a server from the list of servers"""
    server = random.choice(stun_servers_list)
    idx = server.find(":")
    if idx > 0:
        return server[:idx], int(server[idx+1:])
    else:
        return server, 3478


def pick_server():
    """Select a IPv4 Server (need to remove IPv6 addresses)"""
    for i in range(10):
        server, port = pick_server_name()

        try:
            possibilities = socket.getaddrinfo(server, port,
                family = socket.AF_INET,
                type=socket.SOCK_DGRAM
            )
        except socket.gaierror:
            continue
        logger.debug(
            "There are %i possible IPv4 addresses",
            len(possibilities)
        )
        break
    poss = random.choice(possibilities)
    logger.info("Connecting to %s", str((server, port)))
    family, _type, proto, cannoname, sockaddr = poss
    logger.debug("Using address is %s", str(sockaddr))
    return sockaddr
