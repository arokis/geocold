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
    GN = rdflib.Namespace('http://www.geonames.org/ontology#')
    OWL = rdflib.Namespace('http://www.w3.org/2002/07/owl#')
    WG84 = rdflib.Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')


    mapping = {
        'labels' : [
            GNDO.preferredNameForThePlaceOrGeographicName, 
            GN.name
            ],
        'coordinates' : {
            GEO.asWKT : {
                'regex' : r'Point \(\s?(\+[\d.]+)\s(\+[\d.]+)\s?\)',
                'groups': ['long', 'lat']
                },
            WG84.lat  : 'lat',
            WG84.long : 'long'
            },
        'sameAs' : [OWL.sameAs]
        }
    
    """
    uri = bag_of_uris[15]
    
    response = geocold.request(uri, headers=headers)
    print uri + ' > status-code: ' + str(response.status_code) + ' > content: ' + response.content_type
    """

    
    for uri in unified_bag:
        try:
            print geocold.http_lookup(uri, headers, mapping).__dict__
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
