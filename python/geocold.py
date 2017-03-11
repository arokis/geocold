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
import requests
import rdflib
from rdflib.namespace import RDF

class Response():
     def __init__(self, status, header, content):
         self.status_code = status
         self.response_header = header
         self.content = content 
         self.content_type = header.get('content-type')


class Entity():
    def __init__(self, uri):
        self.uri = uri
        self.type = 'unknown'

    
class SilentEntity(Entity):
    status = 'inactive'

    def __init__(self, uri):
        Entity.__init__(self, uri)
        

class ActiveEntity(Entity):
    status = 'active'

    def __init__(self, uri):
        Entity.__init__(self, uri)
        self.sameAs = list()
        self.cls = list()
    
    def classify(self, graph):
        uri = self.uri
        if (uri, RDF.type, None):
            fail = True
            for obj_class in graph.objects( rdflib.URIRef(uri), RDF.type ):
                fail = obj_class
                self.cls = str(obj_class)
            if fail: # check for trailing slash like in geonames-data
                for obj_class in graph.objects( rdflib.URIRef(uri+'/'), RDF.type ):
                    fail = obj_class
                    self.cls = str(obj_class)
        else: # bruteforcing all rdf:types and objects
            for s, p, o in graph:
                print s
                if self.uri in s and p == RDF.type:
                    self.cls.append({str(s) : o})

    def identify(self, graph, mapping):
        #self.mapping = mapping
        coordinates = [key for key in mapping['coordinates']]
        self.classify(graph)
        for s,p,o in graph:
            #print s,p,o
            o = str(o.encode('utf-8'))
            #self.classify(s, p, o)
            self.same(p, o, mapping['sameAs'])
            self.name_me(p, o, mapping['labels'])
            self.find_coordinates(p, o, mapping['coordinates'])
            
    def name_me(self, pred, obj, mapping):
        if pred in mapping:
            self.label = obj

    def same(self, pred, obj, same):
        if pred in same:
            self.sameAs.append(obj) 

    def find_coordinates(self, pred, obj, coord_mapping):
        if pred in coord_mapping:
            self.type = 'place'
            try: # for all more complex matchings
                regex = re.compile(coord_mapping[pred].get('regex'))
                group = coord_mapping[pred].get('groups')
                match = regex.match(obj)
                
                if match:
                    setattr(self, group[0], match.group(1))
                    setattr(self, group[1], match.group(2))
                else: 
                    self.coordinates = obj
                
            except: # if no regex is provided then we will deal with single properties and simple mappings
                value = coord_mapping[pred]
                setattr(self, value, obj)
                


def bagify(data):
    """
    Creates a bag of individual uris from RDF-Data
    
    ARG:
    * data: rdf-data from file or string

    RETURNS:
    * [LIST]: a list containing all subject- and object-URIs
    """
    bag = dict()
    graph = read_rdf(data)
    if graph:
        all_uris = collect_uris(graph)
        bag['original-count'] = len(all_uris)
        unified_bag = individuate(all_uris)
        bag['individuals'] = unified_bag 
        return bag
    else:
        bag['error'] = {'source' : 'geocold.bagify', 'description' : 'Error while collecting uris. Check log-files!'}
        return bag


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


def http_lookup(url, headers, mapping_dict):
    r = request(url, headers=headers)
    #print request.status_code
    if 200 >= r.status_code <= 299 and 'application/rdf+xml' in r.content_type:
        #print r.target + ' > status-code: ' + str(r.status_code) + ' > content: ' + r.content_type
        graph = read_rdf(r.content)
        entity = ActiveEntity(url)
        entity.identify(graph, mapping_dict)
        return entity
    else:
        silent_entity = SilentEntity(url)
        silent_entity.type = 'silent'
        silent_entity.status_code = r.status_code
        #silent_entity.content_type = r.content_type
        return silent_entity


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
    """
    parses RDF-Data from file
    
    ARG:
    * file_path: path to a file

    RETURNS:
    * rdf.lib.Graph: Success -> a RDF-Graph-Object is returned
    * False (bool): An Error occured while parsing
    """
    graph = rdflib.Graph()
    # guess the files format and build the graph
    result = False
    #print 'test'
    try:
        rdf_format = rdflib.util.guess_format(file_path)
        result = graph.parse(file_path, format=rdf_format)
    except AttributeError:
        try:
            #print ('[GeoCoLD:RDF-PARSING]: Error in guessing format. Working on default (application/rdf+xml)!')
            result = graph.parse(file_path)
        except SAXParseException:
            print "[GEOCOLD:ERROR] in parse_rdf_file(): SAXParseException was raised. File is not a valid xml file!"
            pass
    return result


def read_rdf(source):
    """
    evaluates if RDF source is file or string.
    If the Source is a string a temporary file will be created rdflib.parse() can read from.
    
    ARG:
    * source: path of a source
    RETURNS:
    * rdf.lib.Graph: Success -> a RDF-Graph-Object is returned
    * False (bool): An Error occured while parsing
    """
    #print type(source)
    if os.path.isfile(source) and not os.path.isdir(source):
        return parse_rdf_file(source)
    else:
        tmp = tempfile.TemporaryFile()
        try:
            tmp.write(source.encode('utf-8'))
        except UnicodeDecodeError: # catching errors like "UnicodeDecodeError: 'ascii' codec can't decode byte 0xcc in position 2685: ordinal not in range(128)"
            tmp.write(source)
        tmp.seek(0)
        output = parse_rdf_file(tmp)
        tmp.close()
        return output
    

def request(uri, headers=False):
    #print 'URI: ' + uri
    response = ''
    if not headers:
        response = requests.get(uri)
    else:
        response = requests.get(uri, headers=headers)
    
    
    status_code = response.status_code
    response_header = response.headers
    content_type = response_header.get('content-type')
    encoding = response.encoding
    if encoding == None:
        print '[geocold.request()]: Warning! No encoding specified by server. working with UTF-8'
        encoding = 'UTF-8'
    content = response.text.encode(encoding)

    resp = Response(status_code, response_header, content)
    resp.target = uri
    return resp


#############################
###     MAIN & Tests      ###
#############################
"""
rdflib:
* Documentation: http://rdflib.readthedocs.io/en/stable/index.html
* Tutorial & Examples: http://semanticweb.org/wiki/Getting_data_from_the_Semantic_Web.html

requests HTTP-Lib
* Documentation: http://docs.python-requests.org/en/master/
"""

headers = {
    'user-agent': 'GeoCoLD/0.0.1',
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


def testing():
    #Simple testing area

    uri_list = ['http://sws.geonames.org/2918632']

    rdf_type = rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')


    for uri in uri_list:
        resp = request(uri, headers=headers)
        graph = read_rdf(resp.content)
        for s, p, o in graph:
            print s, p , o

        if (rdflib.URIRef(uri), rdf_type, None):
            print uri
            print 'JA, diese Uri hat einen typ'
        #for s,p,o in graph.triples( (rdflib.URIRef(uri), rdf_type, None) ):
        #    print s, o
        
        fail = True
        for obj_class in graph.objects( rdflib.URIRef(uri), rdf_type ):
            fail = obj_class
            print "uri is a %s"%obj_class
        
        if fail:
           for obj_class in graph.objects( rdflib.URIRef(uri+'/'), rdf_type ):
            fail = obj_class
            print "uri is a %s"%obj_class 
        
def full_test():
    pass

def main():
       
    liste = list()
    for uri in uris:
        result = http_lookup(uri, headers, mapping)
        try:
            if result.type == 'unknown' and len(result.sameAs) > 0:
                print 'NEUER VERSUCH MÖGLICH: (' + str(len(result.sameAs)) + ')'
                print result.sameAs
                print result.__dict__
            elif result.type == 'place':
                print 'IDENTIFIZIERT: '
                print result.__dict__
            else: 
                print 'unbekannt: ' + result.uri
        except AttributeError:
            pass

        #print json.dumps(result.__dict__)
        #liste.append(result.__dict__)
    
        print '###'
    #print liste
    
    """
    r = request('http://d-nb.info/gnd/4007879-6', headers=headers)
    #print r.content
    
    if 200 >= r.status_code <= 299 and 'application/rdf+xml' in r.content_type:
        #print r.target + ' with ' + str(r.status_code) + ' as ' + r.content_type
        graph = read_rdf(r.content)
        print_graph(graph)
    """
    

if __name__ == '__main__':
    main()
    #testing()