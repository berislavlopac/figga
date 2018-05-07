#!/usr/bin/env python3
from setuptools import setup

with open('README.md') as readme:
    long_desc = readme.read()

setup(
    name="figga",
    version="0.1.0dev",
    description="A simple configuration manager for Python.",
    long_description=long_desc,
    author="Berislav Lopac",
    url="https://github.com/berislavlopac/figga",
    package_dir={'': 'figga'},
    python_requires=">=3.6",
)
