import os
import logging


def get_to_address():
    fpath = os.path.join("/etc", "wheres_home", "email")
    with open(fpath) as infp:
        name = infp.read().strip()
    logging.debug("Using Email address '%s'" % name)
    return name


def sendMail(msg):
    sendmail_location = "/usr/sbin/sendmail"  # sendmail location
    p = os.popen("%s -t" % sendmail_location, "w")
    name = get_to_address()
#    p.write("From: %s\n" % name)
    p.write("To: %s\n" % name)
    p.write("Subject: %s\n" % msg)
    p.write("\n")  # blank line separating headers from body
    status = p.close()
    if status is not None:
        logging.warn("Sendmail exit status was %s" % str(status))

if __name__ == "__main__":
    sendMail("10.0.0.1")
