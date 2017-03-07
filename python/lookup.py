#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tempfile
import re
import json
import requests
import rdflib

from flask import Flask, request
from flask import make_response
from flask_cors import CORS
app = Flask(__name__)
CORS(app)




def parse_rdf(file_path, format_default='application/rdf+xml'):
    graph = rdflib.Graph()
    return graph.parse(file_path, format=format_default)


def coord_from_pred(graph, dic):
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
            regex = re.compile(dic['coordinates'][p])
            match = regex.match(o)
            if match:
                geo_object['coordinates'] = {'lat': match.group(1), 'long': match.group(2)}
            else:
                geo_object['coordinates'] = o
    return geo_object


def http_lookup(url, headers, mapping_dict):
    r = requests.get(url, headers=headers)
    #print r.text
    tmp = tempfile.TemporaryFile()
    tmp.write(r.text.encode('utf-8'))
    tmp.seek(0)
    #print tmp.read()
    graph = parse_rdf(tmp)
    #print coord_from_pred(graph, kv)
    obj = coord_from_pred(graph, mapping_dict)
    tmp.close()
    return obj


@app.route("/lookup", methods=['GET', 'POST'])
#@crossdomain(origin='*')
def lookup():
    if request.method == 'POST':

        input_url = json.loads(request.form['url'])
        print input_url
        #print type(input_url)

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


        output = ''
        if isinstance(input_url, list):
            out_list = list()
            for url in input_url:
                out_list.append(http_lookup(url, headers, mapping))
            output = json.dumps(out_list)
        else:
            output = json.dumps(http_lookup(input_url, headers, mapping))

        print output
        #resp = make_response('{"response": ' + output + '}')
        resp = make_response( output )
        resp.headers['Content-Type'] = "application/json"
        return resp


if __name__ == '__main__':
    app.run(debug=True)
    #lookup()



"""
Python code  -- app.py 

from flask import Flask, render_template, redirect, url_for,request
from flask import make_response
app = Flask(__name__)

@app.route("/")
def home():
    return "hi"
@app.route("/index")

@app.route('/login', methods=['GET', 'POST'])
def login():
   message = None
   if request.method == 'POST':
        datafromjs = request.form['mydata']
        result = "return this"
        resp = make_response('{"response": '+result+'}')
        resp.headers['Content-Type'] = "application/json"
        return resp
        return render_template('login.html', message='')
if __name__ == "__main__":
app.run(debug = True)
"""