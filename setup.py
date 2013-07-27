#!/usr/bin/env python

from distutils.core import setup

setup(
    name='arkos-beacon',
    version='0.1',
    install_requires=['pyOpenSSL', 'pam'],
    description='Broadcasts arkOS presence and allows for lowlevel config',
    author='The CitizenWeb Project',
    author_email='jacob@citizenweb.is',
    packages=['beacon'],
    url='http://arkos.io/dev/beacon',
    scripts=['beacond'],
    data_files=[
        ('/usr/lib/systemd/system', ['beacon.service']),
    ],
)
