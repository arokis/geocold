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
from collections import OrderedDict
import json
import rdflib
from rdflib.namespace import RDF

# EXCEPTIONS import
from xml.sax import SAXParseException
from rdflib.exceptions import ParserError



def create_bag(bag):
    """
    Creates a dictionary with original subject-object count and doublets-checked http-URIs
    
    ARG:
    * graph: a rdflib.graph object

    RETURNS:
    * {DICT}
    """
    uri_bag = dict()
    complete_list = bag['subjects'] + bag['objects']
    uri_bag['original-count'] = len(complete_list)
    individual_list = [str(i) for i in complete_list if not i.startswith('file:') and isinstance(i, rdflib.term.URIRef)]  
    uri_bag['individuals'] = list(OrderedDict.fromkeys(individual_list))
    #return individual_list
    return uri_bag


def collect_uris(graph):
    """
    Creates a dictionary with subject and object-URIs
    
    ARG:
    * graph: a rdflib.graph object

    RETURNS:
    * {DICT}: a dictionary containing all subject- and object-URIs
    """
    bag = dict()
    subjects = []
    predicates = []
    objects = []

    for s, p, o in graph:
        if not isinstance(s, rdflib.term.Literal):
            subjects.append(s)
        if not isinstance(o, rdflib.term.Literal):
            objects.append(o)
    
    bag['subjects'] = list(OrderedDict.fromkeys(subjects))
    bag['objects'] = list(OrderedDict.fromkeys(objects))
    return bag


def extract_tripple_sets(graph):
    """
    Splits graph into separate tripple-sets according to all subject-URIs
    
    ARG:
    * graph: a rdflib.graph object

    RETURNS:
    * [LIST] with rdflib.graphs: a list containing all subject tripple-sets as rdflib.graphs
    """
    graph_list = []
    for subject in collect_uris(graph)['subjects']:
        single_graph = rdflib.Graph()
        for s,p,o in graph.triples( (subject, None, None) ):
            single_graph.add( (s,p,o) )
        
        if len(single_graph) != 0: 
            graph_list.append(single_graph)
            print_graph(single_graph)
    return graph_list


def mime_mapping(mime):
    """
    mapps mime-types to rdflib-mimes
    
    ARG:
    * mime: a mime-type

    RETURNS:
    * rdflib-mime-type
    """
    result = {
        'application/rdf+xml': 'xml',
        'text/turtle': 'turtle'
        }.get(mime, 'xml')
    
    print ('[GEOCOLD:RDF-PARSER] mapping "' + mime + '" to rdflib-mime "' + result + '"')
    return result


def print_graph(graph):
    print ('Graph (length: ' + str(len(graph)) + '):')
    for s, p, o in graph:
        print (s, p, o.encode(sys.stdout.encoding, errors='replace'))
    print ('')


def rdf_from_file(file_path):
    """
    reads RDF-Data from file and tries to guess mime-type based on file-extension
    
    ARG:
    * file_obj: ...
    * mime: a mime-type

    RETURNS:
    * rdflib.GRAPH
    """
    print ('[GEOCOLD:RDF-PARSER] reading RDF-data from file-object')
    mime = rdflib.util.guess_format(file_path)
    parsed = rdf_graph(file_path, mime=mime) 
    return parsed


def rdf_from_string(data, mime):
    """
    reads RDF-Data from a string and maps given mime-type to rdflib.mimes
    
    ARG:
    * data: rdf-data string
    * mime: a mime-type

    RETURNS:
    * rdflib.GRAPH
    """
    print ('[GEOCOLD:RDF-PARSER] reading RDF-data from string')
    mime = mime_mapping(mime)
    tmp = tempfile.TemporaryFile()
    try:
        tmp.write(data.encode('utf-8'))
    except UnicodeDecodeError: # catching errors like "UnicodeDecodeError: 'ascii' codec can't decode byte 0xcc in position 2685: ordinal not in range(128)"
        tmp.write(data)
    tmp.seek(0)
    parsed = rdf_graph(tmp, mime=mime)
    tmp.close()
    return parsed


def rdf_graph(file_object, mime="application/rdf+xml"):
    """
    parses RDF-Data from file
    
    ARG:
    * file_object: path to a file or tmp-file-object

    RETURNS:
    * rdf.lib.Graph: Success -> a RDF-Graph-Object is returned
    * Error-DICT: An Error occured while parsing
    """
    #print type(file_object)
    print ('[GEOCOLD:RDF-PARSER] parsing RDF (' + mime + ') to Graph')
    
    graph = rdflib.Graph()
    result = False
    try:
        result = graph.parse(file_object, format=mime)
        return result
    except ParserError:
        print ("[GEOCOLD:RDF-PARSER] RDFLib.ParserException was raised. File is not a valid RDF file!")
        return {'error': {'source' : 'rdf_graph', 'description' : 'not a valid RDF file'}}
    
    except SAXParseException:
        print ("[GEOCOLD:RDF-PARSER] XML.sax.SAXParseException was raised. File is not a valid xml file!")
        return {'error': {'source' : 'rdf_graph', 'description' : 'not a valid XML file'}}
        
        

if __name__ == '__main__':
    import time
    start = time.time()

    string = """
    @prefix schema: <http://schema.org/> .
    @prefix gndo: <http://d-nb.info/standards/elementset/gnd#> .
    @prefix lib: <http://purl.org/library/> .
    @prefix marcRole: <http://id.loc.gov/vocabulary/relators/> .
    @prefix owl: <http://www.w3.org/2002/07/owl#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix dcmitype: <http://purl.org/dc/dcmitype/> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix geo: <http://www.opengis.net/ont/geosparql#> .
    @prefix umbel: <http://umbel.org/umbel#> .
    @prefix dbp: <http://dbpedia.org/property/> .
    @prefix dnbt: <http://d-nb.info/standards/elementset/dnb#> .
    @prefix rdau: <http://rdaregistry.info/Elements/u/> .
    @prefix sf: <http://www.opengis.net/ont/sf#> .
    @prefix dnb_intern: <http://dnb.de/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix v: <http://www.w3.org/2006/vcard/ns#> .
    @prefix dcterms: <http://purl.org/dc/terms/> .
    @prefix bibo: <http://purl.org/ontology/bibo/> .
    @prefix gbv: <http://purl.org/ontology/gbv/> .
    @prefix isbd: <http://iflastandards.info/ns/isbd/elements/> .
    @prefix foaf: <http://xmlns.com/foaf/0.1/> .
    @prefix dc: <http://purl.org/dc/elements/1.1/> .

    <http://d-nb.info/gnd/4007879-6> a gndo:TerritorialCorporateBodyOrAdministrativeUnit ;
        foaf:page <http://de.wikipedia.org/wiki/Bovenden> ;
        gndo:gndIdentifier "4007879-6" ;
        gndo:oldAuthorityNumber "(DE-588)2005993-0" ;
        owl:sameAs <http://d-nb.info/gnd/2005993-0> ;
        dnbt:deprecatedUri "http://d-nb.info/gnd/2005993-0" ;
        gndo:oldAuthorityNumber "(DE-588b)2005993-0" , "(DE-588c)4007879-6" ;
        gndo:relatedDdcWithDegreeOfDeterminacy2 <http://dewey.info/class/2--435972/> ;
        owl:sameAs <http://sws.geonames.org/2945726> ;
        geo:hasGeometry _:node1baj4vptax129366 .

    _:node1baj4vptax129366 geo:asWKT "Point ( +009.929959 +051.591799 )"^^geo:wktLiteral ;
        a sf:Point .

    <http://d-nb.info/gnd/4007879-6> gndo:geographicAreaCode <http://d-nb.info/standards/vocab/gnd/geographic-area-code#XA-DE-NI> , <http://d-nb.info/standards/vocab/gnd/geographic-area-code#XA-DXDE> ;
        gndo:biographicalOrHistoricalInformation "Gemeinde im Landkreis Göttingen in Südniedersachsen; ehemals Teil der hessischen Herrschaft Plesse"@de ;
        gndo:variantNameForThePlaceOrGeographicName "Flecken Bovenden" ;
        gndo:preferredNameForThePlaceOrGeographicName "Bovenden" .


    """
    
    f = ['../../data/4007879-6_lds.ttl', '../../data/fontante-register.rdf']
    #graph = rdf_graph(f, mime='n3')
    #graph = rdf_from_string(string, mime="text/turtle")
    graph = rdf_from_file(f[1])
    print_graph(graph)
    print ('')
    print ('URIS:')
    print (collect_uris(graph))
    print ('')
    singles = extract_tripple_sets(graph)
    print singles
    print ('Individuals:')
    di = collect_uris(graph)
    uri_bag = create_bag(di)
    print uri_bag
    print len(uri_bag['individuals'])

    end = time.time()
    print (end - start)