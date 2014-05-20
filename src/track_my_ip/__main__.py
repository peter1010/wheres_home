import sys

print(sys.path)

from . import stun
import time
import os

CACHE_FILE="/var/cache/track_my_ip/history.txt"

def get_last():
    try:
        with open(CACHE_FILE) as in_fp:
            for line in in_fp:
                line.strip()
                if line:
                    non_blank = line
    except FileNotFoundError:
        return None, None
    return non_blank.split()[0]


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
    ip_addr = stun.do_stun_transaction()
    old_ip_addr = get_last()
    if old_ip_addr != ip_addr:
        record(ip_addr)
    print("hello")

run()
