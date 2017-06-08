import os
from setuptools import find_packages, setup


# Utility function to read the README file.  Used for the
# long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put
# a raw string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="statusbar",
    version="0.1.22",

    packages=find_packages(),

    test_suite='tests',
    install_requires=[
        "termcolor>=1.1.0",
    ],

    # metadata for upload to PyPI
    author="Thomas Mailund",
    author_email="mailund@birc.au.dk",
    license="GPLv3",
    keywords="CLI status output",
    url="https://github.com/mailund/statusbar",
    description="Module for displaying (text based) status update lines.",
    long_description=read('README.rst'),

    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",    # NOQA
        "Programming Language :: Python",
    ],
)
