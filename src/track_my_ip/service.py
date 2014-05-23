
def create_group(group):
    import grp, subprocess
    try:
        info = grp.getgrnam(group)
        gid = info.gr_gid
    except KeyError:
        subprocess.call(["groupadd","-K", "GID_MIN=250", group])
        info = grp.getgrnam(group)
        gid = info.gr_gid
    return gid


def remove_group(group):
    import grp, subprocess
    try:
        info = grp.getgrnam(group)
        subprocess.call(["groupdel", group])
    except KeyError:
        pass



def create_user(user, gid):
    import pwd, subprocess
    try:
        info = pwd.getpwnam(user)
        uid = info.pw_uid
    except KeyError:
        subprocess.check(["useradd","-K","UID_MIN=250", "-g", gid, "-s", "/bin/false". user])
        info = pwd.getpwnam(user)
        uid = info.pw_uid
    return uid


def remove_user(user):
    import pwd, subprocess
    try:
        info = pwd.getpwnam(user)
        subprocess.check(["userdel". user])
    except KeyError:
        pass


def start_service():
    create_group("track_my_ip")
    create_user("track_my_ip")
    subprocess.call(["systemctl","enable","track_my_ip.timer"])
    subprocess.call(["systemctl","start","track_my_ip.timer"])


def stop_service():
    subprocess.call(["systemctl","stop","track_my_ip.timer"])
    subprocess.call(["systemctl","disable","track_my_ip.timer"])
    remove_user("track_my_ip")
    remove_group("track_my_ip")


