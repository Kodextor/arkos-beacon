#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
    name='arkos-beacond',
    version='0.1',
    install_requires=['pyOpenSSL'],
    description='Broadcasts arkOS presence and allows for lowlevel config',
    author='The CitizenWeb Project',
    author_email='jacob@citizenweb.is',
    url='http://arkos.io/dev/beacon',
    packages = find_packages(),
    package_data={'': ['files/*.*', 'files/*/*.*', 'files/*/*/*.*', 'templates/*.*', 'widgets/*.*', 'layout/*.*']},
    scripts=['beacond'],
    data_files=[
        ('/etc', ['beacon.conf']),
        ('/usr/lib/systemd/system', ['beacond.service']),
    ],
)
