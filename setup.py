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
    author_email='john.vrbanac@linux.com',
    tests_require=[
        "specter",
        "pretend>=1.0.8"
    ],
    install_requires=[
        "falcon",
        "uwsgi",
        "pynsive>=0.2.7",
        "pymongo"
    ],
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup'])
)
