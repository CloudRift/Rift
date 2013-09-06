Rift
====

Rift is a project inspired by the [Netflix Chaos Monkey](http://techblog.netflix.com/2012/07/chaos-monkey-released-into-wild.html) 
project. It is designed to allow an OpenStack consumer to test their solution to various failure scenarios.

Requirements
============

If installing the service on Ubuntu 12.04, you will need the following packages.

    apt-get install build-essential python-dev python-pip


Installation
============

1. Check out the project and install the dependencies in the tools/pip-requires and tools/test-requires. It is 
recommended that you use a virtual environment to isolate Rift from other python applications on your system.

2. Run uwsgi:

    uwsgi --ini uwsgi.ini
    
3. Rift should be running on port 8080
