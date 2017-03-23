import xml.etree.ElementTree
import rdflib
import json
from rdflib.namespace import RDF, RDFS

def read_xml(path):
    with open(path) as myfile:
        content = myfile.readlines()
    return content

def read_gn_dump_range(path, ranges):
    with open(path) as myfile:
        head = [next(myfile) for x in xrange(ranges)]
    return head


def create_file(path, data):
    file = open(path,"w") 
    file.write(data)
    file.close()


def xml_from_string(data):
    
    def get_attributenode(xml, elem, attr, ns):
        try:
            return xml.find(elem, ns).attrib[attr]
        except:
            return None

    def get_textnode(xml, elem, ns):
        try:
            return xml.find(elem, ns).text.encode('utf-8')
        except:
            return None

    dump_obj = dict()
    x = xml.etree.ElementTree.fromstring(data)
    ns = {
        'gn': 'http://www.geonames.org/ontology#',
        'wg84': 'http://www.w3.org/2003/01/geo/wgs84_pos#'
        }
    
    dump_obj['name'] = get_textnode(x, './/gn:name', ns)
    dump_obj['uri'] = get_attributenode(x, './/gn:Feature', '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', ns)
    dump_obj['lat'] = get_textnode(x, './/wg84:lat', ns)
    dump_obj['long'] = get_textnode(x, './/wg84:long', ns)
    return dump_obj


def query_rdf(graph):
    qres = graph.query(
    """SELECT ?type ?name ?class
       WHERE {
          ?subj rdf:type ?type .
          ?subj gn:name ?name .
          ?subj gn:featureClass ?class .
       }""")

    
    print len(qres.vars)
    print qres.__dict__
    """
    obj = dict()
    for a in qres.vars:
        obj[str(a)] = str(qres.vars[a]).encode('utf-8')
        print str(a).encode('utf-8')

    print obj
    """
    for a in qres:
        print str(a).encode('utf-8')

def create_dump_obj(graph):
    GEO = rdflib.Namespace('http://www.opengis.net/ont/geosparql#')
    GNDO = rdflib.Namespace('http://d-nb.info/standards/elementset/gnd#')
    GN = rdflib.Namespace('http://www.geonames.org/ontology#')
    OWL = rdflib.Namespace('http://www.w3.org/2002/07/owl#')
    WG84 = rdflib.Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')
    dump_obj = dict()
    dump_obj['uri'] = str(graph.value(predicate=RDF.type, object=GN.Feature))
    dump_obj['class'] = tripple_match(graph=graph, pred=RDF.type)
    dump_obj['name'] = tripple_match(graph=graph, pred=GN.name)
    dump_obj['long'] = tripple_match(graph=graph, pred=WG84.long)
    dump_obj['lat'] = tripple_match(graph=graph, pred=WG84.lat)
    return dump_obj


def tripple_match(graph, pred):
    for s,p,o in graph.triples( (None,  pred, None) ):
        #print "%s is a %s"%(s,o.encode('utf-8'))
        return o.encode('utf-8')


def rdf_from_file(file_path):
    GEO = rdflib.Namespace('http://www.opengis.net/ont/geosparql#')
    GNDO = rdflib.Namespace('http://d-nb.info/standards/elementset/gnd#')
    GN = rdflib.Namespace('http://www.geonames.org/ontology#')
    OWL = rdflib.Namespace('http://www.w3.org/2002/07/owl#')
    WG84 = rdflib.Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')

    graph = rdflib.Graph()
    parsed = graph.parse(file_path)
    
    for s, o, p in parsed:
        print s, o ,p.encode('utf-8')

    obj = create_dump_obj(graph)
    print obj


def iter_dump(file_obj):
    error = 0
    for line in iter(file_obj):
        try:
            xml = xml_from_string(line)

            if xml['long'] == None or xml['lat'] == None:
                print ''
                print xml['uri'] + ' ERRORISH!, errors so far: (' + str(error) + ')'
                error += 1
                with open("error.log", "a") as myfile:
                    myfile.write(xml['uri'] + ' ERRORISH\n')
                    myfile.write(json.dumps(xml))
                    myfile.write('\n')
                print xml    
            else:
                print xml['uri'] + ' OKAY, errors so far: (' + str(error) + ')'
                #with open("error.log", "a") as myfile:
                #    myfile.write(xml['uri'] + ' OKAY\n')       
        except:
            #print 'NO XML'
            pass


def harvest(path):
    f = open(path)
    iter_dump(f)
    f.close()


def main():
    #read_gn_dump_full(path)
    #print len(xml_string)
    #xml_string = read_gn_dump_range(path, 12000)
    #xml = xml_from_string(xml_string)
    #print xml_string
    xml_data = read_xml('test.xml')
    xml = xml_from_string(xml_data[0])
    print xml
    
    
    


if __name__ == '__main__':
    import time
    start = time.time()

    main()
    #rdf_from_file('test.xml')  
    #rdf_from_xml('dumps/all-geonames-rdf.txt')  
    #harvest('dumps/all-geonames-rdf.txt')

    end = time.time()
    print (end - start)