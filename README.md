Rift
====

[![Build Status](https://travis-ci.org/CloudRift/Rift.svg?branch=master)](https://travis-ci.org/CloudRift/Rift) [![Coverage Status](https://coveralls.io/repos/CloudRift/Rift/badge.svg?branch=master)](https://coveralls.io/r/CloudRift/Rift?branch=master)

Rift is a service that enables you to conduct automated reliablity testing against your application's environments.

**NOTE: THIS SERVICE IS A WORK IN PROGRESS IS NON-FUNCTIONAL AT THE MOMENT.**

Requirements
============

If installing the service on Ubuntu 14.04, you will need the following packages.

    sudo apt-get install build-essential python-dev python-pip


Installation
============

1. Check out the project and install the dependencies in the tools/pip-requires and tools/test-requires. It is
recommended that you use a virtual environment to isolate Rift from other python applications on your system.

2. Run uwsgi:

    uwsgi --ini uwsgi.ini

3. Rift should be running on port 8080
