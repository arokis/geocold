#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
geocold.py
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
from werkzeug.http import parse_options_header

import entities as GeoEntities
import request as GeoRequest
import rdf_parser

__all__ = ['Geocold']

#+++++++++++++++#
#   Geocold     #
#+++++++++++++++#
class Geocold():
    """
    Geocold-Class encapsulating all functionalities
    IN WORK!
    """

    # class-variables as defaults for each class-instance
    config = {
        'name' : 'GeoCoLD',
        'version': '0.0.1'
        }
    
    mapping = {
        'labels' : [
            'http://d-nb.info/standards/elementset/gnd#preferredNameForThePlaceOrGeographicName', 
            'http://www.geonames.org/ontology#name'
            ],
        'coordinates' : {
            'http://www.opengis.net/ont/geosparql#asWKT' : {
                'regex' : r'Point \(\s?(\+[\d.]+)\s(\+[\d.]+)\s?\)',
                'groups': ['long', 'lat']
                },
            'http://www.w3.org/2003/01/geo/wgs84_pos#lat'  : 'lat',
            'http://www.w3.org/2003/01/geo/wgs84_pos#long' : 'long'
            },
        'sameAs' : ['http://www.w3.org/2002/07/owl#sameAs']
        }

    headers = {
    'user-agent': '-'.join(( config.get('name'), config.get('version') )),
    'Accept' : 'application/rdf+xml;q=0.9, text/turtle;q=0.8'
    }

    def __init__(self, config=config, db_config=None, mapping=mapping, request_headers=headers):
        """
        primary init-method
        """
        print ("[GEOCOLD] instanciating GEOCOLD")
        self.config = config
        self.db = db_config
        self.mapping = mapping
        self.request_headers = request_headers
        if not self.request_headers.get('user-agent'):
            self.request_headers['user-agent'] = '-'.join(( self.config.get('name'), self.config.get('version') ))
        self.entities = list()


    @classmethod
    def from_config(cls, config):
        """
        secondary init-method to parse config.json
        """
        dictionary = config
        return cls()
    

    def bagify(self, graph):
        """
        Creates a bag of individual uris from RDF-Data

        TO-DO:
        -   Bag should also contain places if places are in the source data.
            Bag(original-count, individuals, places)
        
        ARG:
        * graph: rdf-graph

        RETURNS:
        * [DICT]: a Dictionary containing 
            (1) "original-count" (INT): Count of all uris in source
            (2) "individuals" (LIST): List of individual subject- and object-URIs in source
        """
        print ('[GEOCOLD:BAGIFY] individuating URIs from graph ...')
        bag = dict()
        if graph:
            all_uris = self.collect_uris(graph)
            bag['original-count'] = len(all_uris)
            unified_bag = self.individuate(all_uris)
            bag['individuals'] = unified_bag 
            return bag
        else:
            bag['error'] = {'source' : 'geocold.bagify', 'description' : 'Error while collecting uris. Check log-files!'}
            return bag


    def lookup(self):
        pass


    def db_lookup(self):
        pass


    def web_lookup(self, url):
        """
        looks up the uri on the web
        """
        print ('[GEOCOLD:WEB-LOOKUP] looking up URL ' + url)
        
        # small hack since d-nb-server can't cope with multiple Accept-formats
        if 'http://d-nb.info' in url:
            self.request_headers['Accept'] = 'application/rdf+xml'        
        
        request = GeoRequest.Request()
        request.get(url, headers=self.request_headers)
        if request.okay and 'application/rdf+xml' in request.content_type:
            graph = self.read_rdf(request)
            entity = GeoEntities.ActiveEntity(url)
            entity.identify(graph, self.mapping)
            return entity
        else:
            #print 'Resource is dead'
            silent_entity = GeoEntities.SilentEntity(url)
            silent_entity.type = 'silent'
            silent_entity.status_code = request.status_code
            silent_entity.content_type = request.content_type
            return silent_entity


    def read_rdf(self, source):
        """
        evaluates whether RDF source is file or string.
        If the Source is a string a temporary file will be created rdflib.parse() can read from.
        
        ARG:
        * source: path of a source
        
        RETURNS:
        * rdf.lib.Graph: Success -> a RDF-Graph-Object is returned
        * False (bool): An Error occured while parsing
        """
        #print source
        try:
            if os.path.isfile(source) and not os.path.isdir(source):
                return rdf_parser.rdf_from_file(source)
            else:
                print ('[GEOCOLD:RDF-SOURCE] reading RDF-data from non-file source ')
                data = GeoRequest.Request()
                response = data.get(source, headers=self.request_headers)
                """
                mime = Geocold.mime_mapping(data.content_type)
                tmp = tempfile.TemporaryFile()
                tmp.write(data.content)
                tmp.seek(0)
                output = Geocold.parse_rdf_file(tmp, mime)
                tmp.close()
                """
                return rdf_parser.rdf_from_data(data.content, mime=data.content_type)
        except TypeError:
                print ('[GEOCOLD:RDF-SOURCE] reading RDF-data from Request-Object ')
                """
                mime = Geocold.mime_mapping(source.content_type)
                tmp = tempfile.TemporaryFile()
                tmp.write(source.content)
                tmp.seek(0)
                output = Geocold.parse_rdf_file(tmp, mime)
                tmp.close()
                """
                return rdf_parser.rdf_from_data(source.content, mime=source.content_type)



    @staticmethod
    def collect_uris(graph):
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


    @staticmethod
    def individuate(array):
        """
        Deletes duplicates from a given list
        
        ARG:
        * array: a python list

        RETURNS:
        * [LIST]: a list with individual items
        """
        return list(OrderedDict.fromkeys(array))


    @staticmethod
    def parse_rdf_file(file_path, serialisiation_format):
        """
        parses RDF-Data from file
        
        ARG:
        * file_path: path to a file

        RETURNS:
        * rdf.lib.Graph: Success -> a RDF-Graph-Object is returned
        * False (bool): An Error occured while parsing
        """
        print ('[GEOCOLD:RDF-PARSING] parsing RDF to Graph')
        graph = rdflib.Graph()
        result = False

        try:
            #rdf_format = rdflib.util.guess_format(file_path)
            result = graph.parse(file_path, format=serialisiation_format)
        except TypeError:
            print ("[GEOCOLD:RDF-PARSING] TypeError was raised. No RDF!")
            pass
        except AttributeError:
            try:
                #print ('[GEOCOLD:RDF-PARSING]: Error in guessing format. Working on default (application/rdf+xml)!')
                result = graph.parse(file_path, format=serialisiation_format)
            except SAXParseException:
                print ("[GEOCOLD:RDF-PARSING] in parse_rdf_file(): SAXParseException was raised. File is not a valid xml file!")
                pass
        return result

    
    @staticmethod
    def extract_graphs(uris, source_graph):
        graph_list = []
        for uri in uris:
            single_graph = rdflib.Graph()
            subject = rdflib.URIRef(uri)
            for s,p,o in source_graph.triples( (subject, None, None) ):
                single_graph.add( (s,p,o) )
            
            if len(single_graph) != 0: 
                graph_list.append(single_graph)
                #Geocold.print_graph(single_graph)
        return graph_list


    @staticmethod
    def print_graph(graph):
        for s, p, o in graph:
            print (s,p,o.encode(sys.stdout.encoding, errors='replace'))



#############################
###     MAIN & Tests      ###
#############################
"""
rdflib:
* Documentation: http://rdflib.readthedocs.io/en/stable/index.html
* Tutorial & Examples: http://semanticweb.org/wiki/Getting_data_from_the_Semantic_Web.html
"""

db = {
    'user': 'uwe'
    }

headers = {
    'Accept' : 'application/rdf+xml'
    #'Accept' : 'text/turtle'
    }

GEO = rdflib.Namespace('http://www.opengis.net/ont/geosparql#')
GNDO = rdflib.Namespace('http://d-nb.info/standards/elementset/gnd#')
GN = rdflib.Namespace('http://www.geonames.org/ontology#')
OWL = rdflib.Namespace('http://www.w3.org/2002/07/owl#')
WG84 = rdflib.Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')

files = ['../data/fontante-register.rdf']

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

uris = [        
    'http://d-nb.info/gnd/4021477-1',
    'http://d-nb.info/gnd/4007879-6',
    'http://xmlns.com/foaf/0.1/Organization', 
    'http://d-nb.info/gnd/118789708',
    'http://worldcat.org/entity/work/id/4327837',
    'http://d-nb.info/gnd/4324745-3',
    'http://vocab.deri.ie/orca#Source',
    'http://sws.geonames.org/2918632',
    'http://sws.geonames.org/2867613',
    'http://www.wikidata.org/wiki/Q17515838'
    ]

def main():
    liste = list()
    geocold = Geocold(mapping=mapping)
    print geocold.request_headers

    for uri in uris:
        entity = geocold.web_lookup(uri)
        try:
            if entity.type == 'unknown' and len(entity.sameAs) > 0:
                print ('NEUER VERSUCH MÖGLICH: (' + str(len(entity.sameAs)) + ')')
                print (entity.__dict__)
                print (entity.sameAs)
                """
                for i in entity.sameAs:
                    print 'Checking ' + i + ' ...'
                    next_request = Request(headers=headers)
                    entity = next_request.web_lookup(i, mapping)
                    print entity.__dict__
                """
            elif entity.type == 'place':
                print ('IDENTIFIZIERT: ')
                print (entity.__dict__)
            else: 
                print ('unbekannt: ' + entity.uri)
                #print entity.__dict__
        except AttributeError:
            pass

        #print json.dumps(result.__dict__)
        #liste.append(result.__dict__)
    
        print ('###')
    #print liste


def fontane():
    geocold = Geocold(mapping=mapping)
    #print (geocold.__dict__)
    
    source_graph = geocold.read_rdf(files[0])
    print (source_graph)
    
    uri_bag = geocold.bagify(source_graph) 
    #print (uri_bag)

    graphs = geocold.extract_graphs(uri_bag['individuals'], source_graph)
    c = 1
    for g in graphs:
        print '# Graph-nr: ' + str(c) + ', length: ' + str(len(g))
        geocold.print_graph(g)
        print ''
        c+=1
    
    """
    print li
    for i in li:
        #Geocold.print_graph(i)
        print '#'
        for m in mapping['labels']:
            if (None, m, None) in i:
                print Geocold.print_graph(i) 
    """
    """
    for s,p,o in i.triples( (None, None, None) ):
        if p in mapping['labels']:
            print type(s),type(p),type(o)
    """
    

def web():
    geocold = Geocold(mapping=mapping)
    for uri in uris:
        print (geocold.web_lookup(uri).__dict__)
        print ('')
    

if __name__ == '__main__':
    import time
    start = time.time()

    #main()
    fontane()
    #web()

    end = time.time()
    print (end - start)



