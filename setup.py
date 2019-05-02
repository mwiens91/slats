#!/usr/bin/env python3

from setuptools import setup
from slats.version import NAME, DESCRIPTION, VERSION


# Parse readme to include in PyPI page
with open("README.md") as f:
    long_description = f.read()


def capitalize(s):
    """Capitalize the first letter of a string.

    Unlike the capitalize string method, this leaves the other
    characters untouched.
    """
    return s[:1].upper() + s[1:]


setup(
    name=NAME,
    version=VERSION,
    description=capitalize(DESCRIPTION),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mwiens91/slats",
    author="Matt Wiens",
    author_email="mwiens91@gmail.com",
    license='BSD 3-clause "New" or "Revised License"',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=["slats"],
    entry_points={"console_scripts": ["slats = slats.main:main"]},
    python_requires=">=3.6",
    install_requires=["PyYAML>=5.1b3", "spotipy>=2.4.4"],
)
