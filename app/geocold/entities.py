#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
entities.py
"""

import re
import rdflib
from rdflib.namespace import RDF

__all__ = ['Entity', 'SilentEntity', 'ActiveEntity']

######################################################
#       Geocold - Classes                            #
#       *****************                            #
# - Request(): Wrapper-Class for requests-lib.       #   
#                                                    #
# - Entity() > SilentEntity() | ActiveEntity():      #
#   The Geocold-representation of Entitys incl.      #
#   RDF-parsing, graph-traversion,                   #
#   entity-identification etc.                       #
#                                                    #   
######################################################



#+++++++++++++++#
#   Entity      #
#+++++++++++++++#
class Entity():
    """
    """
    def __init__(self, uri):
        self.uri = uri
        self.type = 'unknown'


class Place(Entity):
    """
    """
    def __init__(self, uri, label, lat, long):
        Entity.__init__(self, uri)
        self.type = 'place'
        self.label = label
        self.coordinates = dict()
        self.coordinates['lat'] = lat
        self.coordinates['long'] = long
    
    def _set_coordinates(self, lat, long).
        pass

    
class SilentEntity(Entity):
    """
    """
    status = 'inactive'

    def __init__(self, uri):
        Entity.__init__(self, uri)
        

class ActiveEntity(Entity):
    """
    """
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
                #print obj_class
                self.cls.append(obj_class.encode('UTF-8'))
            if fail: # check for trailing slash like in geonames-data
                for obj_class in graph.objects( rdflib.URIRef(uri+'/'), RDF.type ):
                    #fail = obj_class
                    self.cls.append(obj_class.encode('UTF-8'))
        else: # bruteforcing all rdf:types and objects
            for s, p, o in graph:
                print (s)
                if self.uri in s and p == RDF.type:
                    self.cls.append({s.encode('UTF-8') : o})

    def identify(self, graph, mapping):
        #self.mapping = mapping
        coordinates = [key for key in mapping['coordinates']]
        self.coordinates = dict()
        self.classify(graph)
        for s,p,o in graph:
            #print s,p,o
            o = str(o.encode('utf-8'))
            #self.classify(s, p, o)
            self.same(p, o, mapping['sameAs'])
            self.name_me(p, o, mapping['labels'])
            self.find_coordinates(p, o, mapping['coordinates'])
        
        # cleanup
        if len(self.coordinates) == 0:
            del self.coordinates
            
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
                    self.coordinates[group[0]] = match.group(1)
                    self.coordinates[group[1]] = match.group(2)
                    #setattr(self, group[0], match.group(1))
                    #setattr(self, group[1], match.group(2))
                else: 
                    self.coordinates = obj
                
            except: # if no regex is provided then we will deal with single properties and simple mappings
                value = coord_mapping[pred]
                #print "EXCEPT: " + value + ' > ' + obj
                self.coordinates[value] = obj
                #setattr(self, value, obj)



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

def query():
    #Simple testing area

    uri_list = ['http://sws.geonames.org/2918632']

    rdf_type = rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')


    for uri in uri_list:
        resp = Request(headers=headers)
        resp.get(uri)

        graph = read_rdf(resp.content)
        for s, p, o in graph:
            print (s, p , o)

        if (rdflib.URIRef(uri), rdf_type, None):
            print (uri)
            print ('JA, diese Uri hat einen typ')
        #for s,p,o in graph.triples( (rdflib.URIRef(uri), rdf_type, None) ):
        #    print s, o
        
        fail = True
        for obj_class in graph.objects( rdflib.URIRef(uri), rdf_type ):
            fail = obj_class
            print ("uri is a %s"%obj_class)
        
        if fail:
           for obj_class in graph.objects( rdflib.URIRef(uri+'/'), rdf_type ):
            fail = obj_class
            print ("uri is a %s"%obj_class)

def main():
       
    liste = list()
    for uri in uris:
        request = Request(headers=headers)
        entity = request.web_lookup(uri, mapping)
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
    




if __name__ == '__main__':
    import time
    start = time.time()

    main()
    

    end = time.time()
    print (end - start)



