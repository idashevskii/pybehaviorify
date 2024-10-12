#!/usr/bin/env python
from distutils.core import setup

setup(
    name='pybehaviorify',
    version='0.0.1',
    description='Lighweight Behaviour Tree',
    packages=[
        'pybehaviorify',
        'pybehaviorify.decorators',
        'pybehaviorify.core',
        'pybehaviorify.composites',
        'pybehaviorify.actions',
    ],
)
