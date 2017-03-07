#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from collections import OrderedDict
import requests
import rdflib


def open_file(path):
    """
    opens files and reads it in with params

    ARGS:
    * path: path of file being opened

    RETURN:
    * content of a file or sys.exit(1)
    """
    try:
        with open(path, 'r') as out:
            output = out.read()
        return output
    except IOError:
        print ('No such File "' + path + '"!')
        sys.exit(1)

def parse_rdf(file_path):
    # guess the files format
    rdf_format = rdflib.util.guess_format(file_path)
    #print rdf_format

    # build the graph and return it
    graph = rdflib.Graph()
    return graph.parse(file_path, format=rdf_format)


def creates_uri_bag(graph):
    bag = list()
    for s, p, o in graph:

        if not isinstance(s, rdflib.term.Literal):
            bag.append(str(s))
        if not isinstance(o, rdflib.term.Literal):
            bag.append(str(o))

    return individuate(bag)


def individuate(array):
    return list(OrderedDict.fromkeys(array))

def main():

    test_xml = '../data/fontante-register.rdf'
    test_ttl = '../data/4007879-6_lds.ttl'

    graph = parse_rdf(test_xml)
    #creates_uri_bag(graph)
    bag_of_uris = creates_uri_bag(graph)
    """
    r = requests.get(bag_of_uris[1])
    status_code = r.status_code
    #print status_code
    #print type(status_code)
    if 200 >= status_code <= 299:
        print bag_of_uris[1] + ' > status-code: ' + str(status_code)
    """

    headers = {
        'user-agent': 'test-app/0.0.1',
        'Accept' : 'application/rdf+xml'
        }

    for uri in bag_of_uris:
        try:
            r = requests.get(uri, headers=headers)
            status_code = r.status_code
            response_header = r.headers
            content_type = response_header.get('content-type')
            #print status_code

            if 200 >= status_code <= 299 and 'application/rdf+xml' in content_type:
                print uri + ' > status-code: ' + str(status_code) + ' > content: ' + content_type
                #print response_header
                #print content_type
                #print r.text
                #print '###'
        except:
            pass


if __name__ == '__main__':
    main()
