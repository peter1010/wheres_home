#!/usr/bin/env python3

import os
import pwd
from distutils.core import setup
from distutils.command import install_data, install


class my_install(install.install):
    def run(self):
        retVal = super().run()
        if self.root is None or not self.root.endswith("dumb"):
            if not os.getenv("DONT_START"):
                from src import service
                service.start_service()
        return retVal;


setup(name='track_my_ip',
      version='1.0',
      description="Keep track of current public IP address",
      url='https://github.com/peter1010/track_my_ip',
      author='Peter1010',
      author_email='peter1010@localnet',
      license='GPL',
      package_dir={'track_my_ip':'src'},
      packages=['track_my_ip'],
      data_files=[\
            ('/usr/lib/systemd/system',
                ('track_my_ip.timer','track_my_ip.service'))],
      cmdclass = {'install' : my_install}
      )
