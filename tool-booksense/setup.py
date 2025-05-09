from setuptools import setup, find_packages

setup(
    name="booksense",
    version="0.1.0",
    description="A collection of tools for managing book data",
    author="CTS285 Team",
    packages=find_packages(),
    install_requires=[
        "pytest>=7.0.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)