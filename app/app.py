#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import requests
import rdflib

import geocold
from flask import Flask, request, render_template
from flask import make_response
from flask_cors import CORS
app = Flask(__name__, static_url_path='/static')
CORS(app)

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates
    

@app.route("/")
#@crossdomain(origin='*')
def home():
    app_title = 'Home'
    return render_template('rdf_input_form.html', title=app_title)


@app.route("/about")
#@crossdomain(origin='*')
def about():
    app_title = 'About'
    return render_template('about.html', title=app_title)


@app.route("/input")
#@crossdomain(origin='*')
def input():
    app_title = 'Input'
    return render_template('rdf_input_form.html', title=app_title)


@app.route("/contact")
#@crossdomain(origin='*')
def contact():
    app_title = 'Contact'
    return render_template('contact.html', title=app_title)


@app.route("/mapsite")
#@crossdomain(origin='*')
def mapsite():
    #POST = request.form['data']
    app_title = 'Mapsite'
    uris = {'individuals' : [
        'http://d-nb.info/gnd/7688136-2',
        'http://d-nb.info/gnd/4021477-1',
        'http://d-nb.info/gnd/4007879-6', 
        'http://d-nb.info/gnd/118789708',
        'http://worldcat.org/entity/work/id/4327837',
        'http://d-nb.info/gnd/4324745-3',
        'http://vocab.deri.ie/orca#Source',
        'http://sws.geonames.org/2918632',
        'http://sws.geonames.org/2867613',
        'http://www.wikidata.org/wiki/Q17515838'
        ]}

    return render_template('mapsite.html', title=app_title, data=uris)


@app.route("/uri", methods=['POST'])
#@crossdomain(origin='*')
def collect_uris():
    POST = request.form['rdf']
    uri_bag = geocold.bagify(POST)
    #print type(POST[0])
    if not 'error' in uri_bag:
        app_title = 'Mapsite'
        #return render_template('uri.html', data=uri_bag)
        return render_template('mapsite.html', title=app_title, data=uri_bag)
    else:
        print(uri_bag)
        return render_template('rdf_input_form.html', error=uri_bag)


@app.route("/lookup", methods=['POST'])
#@crossdomain(origin='*')
def lookup():
    if request.method == 'POST':

        input_url = json.loads(request.form['url'])
        print(input_url)
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
                lookup = geocold.Request(headers=headers)
                entity = lookup.web_lookup(url, mapping_dict=mapping)
                out_list.append(entity.__dict__)
            output = json.dumps(out_list)
        else:
            lookup = geocold.Request(headers=headers)
            entity = lookup.web_lookup(input_url, mapping_dict=mapping)
            output = json.dumps(entity.__dict__)

        print(output)
        #resp = make_response('{"response": ' + output + '}')
        resp = make_response( output )
        resp.headers['Content-Type'] = "application/json"
        return resp


if __name__ == '__main__':
    app.run(debug=True)
