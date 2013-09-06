# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='Rift',
    version='0.1',
    description='',
    author='CLoudRift',
    author_email='jvrbanac@gmail.com',
    tests_require=[
        "nose",
        "coverage",
        "spec",
        "tox"
    ],
    install_requires=[
        "falcon",
        "uwsgi",
        "pynsive",
        "pymongo"
    ],
    test_suite='nose.collector',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup'])
)