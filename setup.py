#!/usr/bin/env python3

from setuptools import setup

setup(name='track_my_ip',
      version='1.0',
      description="Keep track of current public IP address",
      url='https://github.com/peter1010/track_my_ip',
      author='Peter1010',
      license='gpl',
      packages=['src'],
      package_dir={'':'src'},
      data_files=[('/usr/lib/systemd/system','track_my_ip.timer'),
                  ('/usr/lib/systemd/system','track_my_ip.service')]
      )

