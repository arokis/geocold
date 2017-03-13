#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import requests
import rdflib

import geocold
from flask import Flask, request
from flask import make_response
from flask_cors import CORS
app = Flask(__name__)
CORS(app)



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


        output = ''
        if isinstance(input_url, list):
            out_list = list()
            for url in input_url:
                out_list.append(geocold.http_lookup(url, headers, mapping).__dict__)
            output = json.dumps(out_list)
        else:
            output = json.dumps(geocold.http_lookup(input_url, headers, mapping).__dict__)

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