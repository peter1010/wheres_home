import time
import os
import argparse
import logging

from . import stun
from . import notify

CACHE_FILE = "/var/cache/track_my_ip/history.txt"


def get_last():
    last_line = ""
    try:
        with open(CACHE_FILE, "r") as in_fp:
            for line in in_fp:
                line.strip()
                if line:
                    last_line = line
    except FileNotFoundError:
        pass
    parts = last_line.split()
    if len(parts) > 0:
        return parts[0]
    return None


def write_record(out_fp, ip_addr):
    out_fp.write(ip_addr)
    out_fp.write("\t")
    out_fp.write(str(time.time()))
    out_fp.write("\n")


def make_path(pathname):
    if os.path.exists(pathname):
        return
    root = os.path.dirname(pathname)
    if not os.path.exists(root):
        make_path(root)
    os.mkdir(pathname)


def record(ip_addr):
    try:
        with open(CACHE_FILE, "a") as out_fp:
            write_record(out_fp, ip_addr)
    except FileNotFoundError:
        make_path(os.path.dirname(CACHE_FILE))
        with open(CACHE_FILE, "w") as out_fp:
            write_record(out_fp, ip_addr)


def run():
    parser = argparse.ArgumentParser(description="Track My IP")
    parser.add_argument('-d', '--debug', action="store_true", default=False,
                        help="Enable debug")
    args = parser.parse_args()
    log = logging.getLogger()
    if args.debug:
        print("Debug enabled")
        log.setLevel(logging.DEBUG)

    ip_addr = stun.do_stun_transaction()
    old_ip_addr = get_last()
    if old_ip_addr != ip_addr:
        record(ip_addr)
        notify.sendMail(ip_addr)

run()
