#!/usr/bin/env python2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from distutils.core import setup

setup(
    name='libfds',
    version='0.0',
    description="Foxdog Studios's Python library.",

    author='Foxdog Studios',
    author_email='contact@foxdogstudios.com',
    url='http://foxdogstudios.com/',

    package_dir={'': 'src'},
    packages=(
        'fds',
    ),
)
