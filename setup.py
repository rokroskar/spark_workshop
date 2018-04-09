import os

from setuptools import setup, find_packages

setup(
    name='spark_intro',
    version="0.0.1",
    python_requires='>=3.5',
    author='Rok Roškar',
    author_email='roskarr@ethz.ch',
    license='Apache License 2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['jupyter', 'notebook', 'BeautifulSoup4', 'findspark'])
