import os
import logging

def get_to_address():
    fpath = os.path.join("/etc", "track_my_ip", "email")
    with open(fpath) as infp:
        name = infp.read().strip()
    logging.debug("Using Email address '%'" % name)
    return name


def sendMail(msg):
    sendmail_location = "/usr/sbin/sendmail" # sendmail location
    p = os.popen("%s -t" % sendmail_location, "w")
    name = get_to_address()
#    p.write("From: %s\n" % name)
    p.write("To: %s\n" % name)
    p.write("Subject: %s\n" % msg)
    p.write("\n") # blank line separating headers from body
    status = p.close()
    if status != 0:
        logging.warn("Sendmail exit status", status)

if __name__ == "__main__":
    sendMail("10.0.0.1")
