import sys
import grp
import pwd
import subprocess
import os

def create_group(group):
    try:
        info = grp.getgrnam(group)
        gid = info.gr_gid
    except KeyError:
        subprocess.call(["groupadd","-r", group])
        info = grp.getgrnam(group)
        gid = info.gr_gid
    return gid


def remove_group(group):
    try:
        info = grp.getgrnam(group)
        subprocess.call(["groupdel", group])
    except KeyError:
        pass



def create_user(user, gid):
    try:
        info = pwd.getpwnam(user)
        uid = info.pw_uid
    except KeyError:
        subprocess.call(["useradd","-r", "-g", str(gid), 
                "-s", "/bin/false", user])
        info = pwd.getpwnam(user)
        uid = info.pw_uid
    return uid


def remove_user(user):
    try:
        info = pwd.getpwnam(user)
        subprocess.call(["userdel", user])
    except KeyError:
        pass


def make_dir(path, uid, gid):
    if not os.path.exists(path):
        os.mkdir(path)
    os.chown(path, uid, gid)
    for f in os.listdir(path):
        os.chown(os.path.join(path,f), uid, gid)


def start_service():
    gid = create_group("track_my_ip")
    uid = create_user("track_my_ip", gid)
    make_dir(os.path.join("/var","cache", "track_my_ip"), uid, gid)
    subprocess.call(["systemctl","enable","track_my_ip.timer"])
    subprocess.call(["systemctl","start","track_my_ip.timer"])


def stop_service():
    subprocess.call(["systemctl","stop","track_my_ip.timer"])
    subprocess.call(["systemctl","disable","track_my_ip.timer"])
    remove_user("track_my_ip")
    remove_group("track_my_ip")

if __name__ == "__main__":
    if sys.argv[1] == "start":
        start_service()
    else:
        stop_service()