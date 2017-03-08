#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
geocold.py
"""

import tempfile
import os
import re
import sys
from collections import OrderedDict
import json
import requests
import rdflib

class Response():
     def __init__(self, status, header, content):
         self.status_code = status
         self.response_header = header
         self.content = content 
         self.content_type = header.get('content-type')


class Entity():
    def __init__(self, uri):
        self.uri = uri

    
    def same_as(self):
        pass
    



def bag_of_uris(graph):
    """
    Creates a list of uris incl. duplicates
    
    ARG:
    * graph: a rdflib.graph object

    RETURNS:
    * [LIST]: a list containing all subject- and object-URIs
    """
    bag = list()
    for s, p, o in graph:
        if not isinstance(s, rdflib.term.Literal):
            bag.append(str(s))
        if not isinstance(o, rdflib.term.Literal):
            bag.append(str(o))
    return bag


def coord_from_pred(graph, dic):
    """
    naive!
    """
    #print dic
    #geo_list = list()
    geo_object = dict()
    coordinate_keys = [key for key in dic['coordinates']]
    #print dic['coordinates'][coordinate_keys[0]]
    #print coordinate_keys
    for s,p,o in graph:
        o = str(o.encode('utf-8'))
        if p in dic['labels']:
            geo_object['label'] = o
        if p in coordinate_keys:
            #print o
            regex = re.compile(dic['coordinates'][p])
            match = regex.match(o)
            if match:
                geo_object['coordinates'] = {'long': match.group(1), 'lat': match.group(2)}
            else:
                geo_object['coordinates'] = o
    return geo_object


def http_lookup(url, headers, mapping_dict):
    r = request(url, headers=headers)
    #print request.status_code
    if 200 >= r.status_code <= 299 and 'application/rdf+xml' in r.content_type:
        #print r.target + ' > status-code: ' + str(r.status_code) + ' > content: ' + r.content_type
        #print r.target + ' with ' + str(r.status_code) + ' as ' + r.content_type
        graph = parse_rdf_source(r.content)
        #geocold.print_graph(graph)
        obj = coord_from_pred(graph, mapping_dict)
        obj['uri'] = url
        return obj
    else:
        obj = dict()
        obj['uri'] = url
        obj['type'] = 'NONE'
        obj['status-code'] = r.status_code
        obj['content-type'] = r.content_type
        return obj


def individuate(array):
    """
    Deletes duplicates from a given list
    
    ARG:
    * array: a python list

    RETURNS:
    * [LIST]: a list with individual items
    """
    return list(OrderedDict.fromkeys(array))


def print_graph(graph):
    for s, p, o in graph:
        print s,p,o.encode(sys.stdout.encoding, errors='replace')


def parse_rdf_file(file_path):
    graph = rdflib.Graph()
    # guess the files format and build the graph
    try:
        rdf_format = rdflib.util.guess_format(file_path)
        return graph.parse(file_path, format=rdf_format)
    except AttributeError:
        #print ('[GeoCoLD:RDF-PARSING]: Error in guessing format. Working on default (application/rdf+xml)!')
        return graph.parse(file_path)


def parse_rdf_source(source):
    if os.path.isfile(source) and not os.path.isdir(source):
        return parse_rdf_file(source)
    else:
        tmp = tempfile.TemporaryFile()
        tmp.write(source)
        tmp.seek(0)
        output = parse_rdf_file(tmp)
        tmp.close()
        return output
    

def request(uri, headers=False):
    response = ''
    if not headers:
        response = requests.get(uri)
    else:
        response = requests.get(uri, headers=headers)
    
    encoding = response.encoding
    status_code = response.status_code
    response_header = response.headers
    content_type = response_header.get('content-type')
    content = response.text.encode(encoding)

    resp = Response(status_code, response_header, content)
    resp.target = uri
    return resp


#############################
###     MAIN              ###
#############################

def main():
    
    headers = {
            'user-agent': 'GeoCoLD/0.0.1',
            'Accept' : 'application/rdf+xml'
            }

    GEO = rdflib.Namespace('http://www.opengis.net/ont/geosparql#')
    GNDO = rdflib.Namespace('http://d-nb.info/standards/elementset/gnd#')

    geo_asWKT = GEO.asWKT
    gnd_preferedLabel = GNDO.preferredNameForThePlaceOrGeographicName

    mapping = {
        'labels' : gnd_preferedLabel,
        'coordinates' : {
            geo_asWKT : r'Point \(\s?(\+[\d.]+)\s(\+[\d.]+)\s?\)'
            }
        }
    
    uris = [
        'http://d-nb.info/gnd/4021477-1',
        'http://d-nb.info/gnd/4007879-6', 
        'http://d-nb.info/gnd/118789708',
        'http://worldcat.org/entity/work/id/4327837',
        'http://d-nb.info/gnd/4324745-3',
        'http://vocab.deri.ie/orca#Source',
        'http://sws.geonames.org/2918632',
        'http://sws.geonames.org/2867613',
        'http://www.wikidata.org/wiki/Q17515838'
        ]

    for uri in uris:
        result = http_lookup(uri, headers, mapping)
        print result
        print '###'

    """
    r = request('http://d-nb.info/gnd/4007879-6', headers=headers)
    #print r.content
    
    if 200 >= r.status_code <= 299 and 'application/rdf+xml' in r.content_type:
        #print r.target + ' with ' + str(r.status_code) + ' as ' + r.content_type
        graph = parse_rdf_source(r.content)
        print_graph(graph)
    """
    

if __name__ == '__main__':
    main()