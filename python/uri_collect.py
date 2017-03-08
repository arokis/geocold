#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import rdflib
import requests

import geocold


def main():

    test_xml = '../data/fontante-register.rdf'
    test_ttl = '../data/4007879-6_lds.ttl'

    graph = geocold.parse_rdf_file(test_xml)
    #creates_uri_bag(graph)
    bag_of_uris = geocold.bag_of_uris(graph)
    print len(bag_of_uris)
    unified_bag = geocold.individuate(bag_of_uris) 
    print len(unified_bag)
    
    #for i in unified_bag:
    #    print i
    
    headers = {
        'user-agent': 'test-app/0.0.1',
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
    
    """
    uri = bag_of_uris[15]
    
    response = geocold.request(uri, headers=headers)
    print uri + ' > status-code: ' + str(response.status_code) + ' > content: ' + response.content_type
    """

    
    for uri in unified_bag:
        try:
            print geocold.http_lookup(uri, headers, mapping)
            print '###'
            """
            response = geocold.request(uri, headers=headers)
            status_code = response.status_code
            response_header = response.response_header
            content_type = response.content_type
            #print status_code

            if 200 >= status_code <= 299 and 'application/rdf+xml' in content_type:
                print uri + ' > status-code: ' + str(status_code) + ' > content: ' + content_type
                #print response_header
                #print content_type
                #print r.text
                #print '###'
            """
        except:
            #print geocold.http_lookup(uri, headers, mapping)
            pass
    

if __name__ == '__main__':
    main()
