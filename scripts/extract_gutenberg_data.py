#!/usr/bin/env python
"""

Script to extract data from the raw Gutenberg corpus.

Author: Rok Roskar

2014-2018 ETH Zürich

"""
import os

from pathlib import Path

from spark_intro import gutenberg_cleanup

rdf_path = os.environ.get('GUTENBERG_RDF_PATH', Path.cwd() / 'data' / 'rdf')
data_path = '/Volumes/PGDVD_2010_04_RC2/'
extract_path = os.environ.get('GUTENBERG_EXTRACT_PATH',
                              Path.cwd() / 'data' / 'extracted')

gutenberg_cleanup.extract_data(data_path, extract_path)
