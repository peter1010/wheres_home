#!/usr/bin/env python3

import os
from distutils.core import setup
from distutils.command import install


class my_install(install.install):
    def run(self):
        retVal = super().run()
        if self.root is None or not self.root.endswith("dumb"):
            if not os.getenv("DONT_START"):
                from src import service
                service.start_service()
        return retVal


setup(
    name='wheres_home',
    version='1.0',
    description="Keep track of current public IP address",
    url='https://github.com/peter1010/wheres_home',
    author='Peter1010',
    author_email='peter1010@localnet',
    license='GPL',
    package_dir={'wheres_home': 'src'},
    packages=['wheres_home'],
    data_files=[
        ('/usr/lib/systemd/system',
         ('wheres_home.timer', 'wheres_home.service'))
    ],
    cmdclass={'install': my_install}
)
