#!/usr/bin/env python3

import os
import pwd
import subprocess

from distutils.core import setup
from distutils.command import install_data


class my_install_data(install_data.install_data):
    def run(self):
        retVal = super().run()
        for path in self.outfiles:
            if path.startswith("/var"):
                o = pwd.getpwnam("nobody")
                os.chown(path, o.pw_uid, o.pw_gid)
        print( self.outfiles)
        subprocess.call(["systemctl","enable","track_my_ip.timer"])
        subprocess.call(["systemctl","start","track_my_ip.timer"])


setup(name='track_my_ip',
      version='1.0',
      description="Keep track of current public IP address",
      url='https://github.com/peter1010/track_my_ip',
      author='Peter1010',
      author_email='peter1010@localnet',
      license='GPL',
      packages=['track_my_ip'],
      package_dir={'':'src'},
      data_files=[\
            ('/usr/lib/systemd/system',
                ('track_my_ip.timer','track_my_ip.service')),
            ('/var/cache/track_my_ip',[])],
      cmdclass = {'install_data': my_install_data}
      )

