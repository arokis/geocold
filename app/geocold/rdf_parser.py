#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
geocold/rdf-parser.py

parsing functionalities for rdf-data
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


def mime_mapping(mime):
    """
    mapps mime-types to rdflib-mimes
    
    ARG:
    * mime: a mime-type

    RETURNS:
    * rdflib-mime-type
    """
    #print mime
    mime_map = {
        'application/rdf+xml': 'xml',
        'text/turle': 'n3'
        }
    result = mime_map.get(mime, 'xml')
    print ('[GEOCOLD:RDF-PARSER] mapping "' + mime + '" to rdflib-mime "' + result + '"')
    return result


def rdf_from_file(file_obj, mime=None):
    """
    ...
    
    ARG:
    * file_obj: ...
    * mime: a mime-type

    RETURNS:
    * rdflib.GRAPH
    """
    print ('[GEOCOLD:RDF-PARSER] reading RDF-data from file-object')
    if mime == None:
        mime = rdflib.util.guess_format(file_obj)
    graph = rdflib.Graph()
    parsed = graph.parse(file_obj, format=mime) 
    return parsed
    #return Geocold.parse_rdf_file(file_path, mime)


def rdf_from_string(data, mime="xml"):
    """
    ...
    
    ARG:
    * data: ...
    * mime: a mime-type

    RETURNS:
    * rdflib.GRAPH
    """
    print ('[GEOCOLD:RDF-PARSER] reading RDF-data from string')
    mime = mime_mapping(mime)
    tmp = tempfile.TemporaryFile()
    tmp.write(data)
    tmp.seek(0)
    parsed = rdf_from_file(tmp, mime)
    tmp.close()
    return parsed