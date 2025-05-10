#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for the Dataman package.
"""
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="dataman",
    version="0.3.1",
    author="Dataman Team",
    author_email="dataman@example.com",
    description="A math problem solver and trainer application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tool-dataman",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "dataman-cli=dataman.interfaces.cli.dataman_cli:main",
        ],
    },
)