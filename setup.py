#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pyusb==1.0.0',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pyluxafor',
    version='0.2.0',
    description="Python API for the Luxafor Flag",
    long_description=readme + '\n\n' + history,
    author="Tom Smith",
    author_email='tom@takeontom.com',
    url='https://github.com/takeontom/pyluxafor',
    packages=[
        'pyluxafor',
    ],
    package_dir={'pyluxafor':
                 'pyluxafor'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pyluxafor',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
