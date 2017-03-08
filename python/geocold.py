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
    
    def classify(self, subj, pred, obj):
        #print subj
        #print self.uri
        if self.uri in subj and pred == RDF.type:
            self.cls.append({str(subj) : obj})

    def identify(self, graph, mapping):
        #self.mapping = mapping
        coordinates = [key for key in mapping['coordinates']]
        for s,p,o in graph:
            #print s,p,o
            o = str(o.encode('utf-8'))
            self.classify(s, p, o)
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
            try: # fro all more complex matchings
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


def http_lookup(url, headers, mapping_dict):
    r = request(url, headers=headers)
    #print request.status_code
    if 200 >= r.status_code <= 299 and 'application/rdf+xml' in r.content_type:
        #print r.target + ' > status-code: ' + str(r.status_code) + ' > content: ' + r.content_type
        graph = parse_rdf_source(r.content)
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
        'http://d-nb.info/gnd/118789708',
        'http://worldcat.org/entity/work/id/4327837',
        'http://d-nb.info/gnd/4324745-3',
        'http://vocab.deri.ie/orca#Source',
        'http://sws.geonames.org/2918632',
        'http://sws.geonames.org/2867613',
        'http://www.wikidata.org/wiki/Q17515838'
        ]
    
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
        graph = parse_rdf_source(r.content)
        print_graph(graph)
    """
    

if __name__ == '__main__':
    main()