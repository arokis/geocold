#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
geocold/functions.py

general functionalities for rdf-data
"""

import tempfile
import os
import re
import sys
from xml.sax import SAXParseException
from collections import OrderedDict
import json
import rdflib
from rdflib.namespace import RDF

