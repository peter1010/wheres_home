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
        subprocess.call(["groupadd", "-r", group])
        info = grp.getgrnam(group)
        gid = info.gr_gid
    return gid


def remove_group(group):
    try:
        grp.getgrnam(group)
        subprocess.call(["groupdel", group])
    except KeyError:
        pass


def create_user(user, home, gid):
    try:
        info = pwd.getpwnam(user)
        uid = info.pw_uid
    except KeyError:
        subprocess.call(["useradd", "-r", "-g", str(gid),
                        "-s", "/bin/false", "-d", home, user])
        info = pwd.getpwnam(user)
        uid = info.pw_uid
    return uid


def remove_user(user):
    try:
        pwd.getpwnam(user)
        subprocess.call(["userdel", user])
    except KeyError:
        pass


def make_dir(path, uid, gid):
    if not os.path.exists(path):
        os.mkdir(path)
    if uid is not None:
        os.chown(path, uid, gid)
        for f in os.listdir(path):
            os.chown(os.path.join(path, f), uid, gid)


def start_service():
    home = os.path.join("/var", "cache", "wheres_home")
    gid = create_group("wheres_home")
    uid = create_user("wheres_home", home, gid)
    make_dir(home, uid, gid)
    make_dir(os.path.join("/etc", "wheres_home"), None, None)
    subprocess.call(["systemctl", "enable", "wheres_home.timer"])
    subprocess.call(["systemctl", "start", "wheres_home.timer"])


def stop_service():
    subprocess.call(["systemctl", "stop", "wheres_home.timer"])
    subprocess.call(["systemctl", "disable", "wheres_home.timer"])
    remove_user("wheres_home")
    remove_group("wheres_home")

if __name__ == "__main__":
    if sys.argv[1] == "start":
        start_service()
    else:
        stop_service()
