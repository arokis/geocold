#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
request.py
"""

import requests
from werkzeug.http import parse_options_header

__all__ = ['Request']

#+++++++++++++++#
#   Request     #
#+++++++++++++++#
class Request():
    """
    Wrapper-Class for requests-lib
    """
    def __init__(self):
        self.url = None
        self.okay = False
        self.content = None
        self.content_type = None
        self.redirects = None
    
    def get(self, url, headers=False):
        """
        gathers the responded data, like instance.content if the url is not a bad request or the instance.content_type
        """
        self.url = url
        
        response = ''
        if not headers:
            response = requests.get(url)
        else: 
            response = requests.get(url, headers=headers)

        self.okay = self.__eval_status(response)
        self.redirects = [redirect.url for redirect in response.history]
        content_type = response.headers.get('content-type')
        self.content_type = parse_options_header(content_type)[0]
        self.status_code = response.status_code
        if self.okay:
            self.content = self.__get_content(response)
        # requests-lib API to interface the response object if needed
        return response

    def __eval_status(self, response):
        return response.status_code == requests.codes.ok 

    def __get_content(self, response):
        encoding = response.encoding
        if encoding == None:
            print ('[GEOCOLD:REQUEST] Warning! No encoding specified by server. working with UTF-8')
            encoding = 'UTF-8'
        return response.text.encode(encoding)


#############################
###     MAIN & Tests      ###
#############################
"""
requests HTTP-Lib
* Documentation: http://docs.python-requests.org/en/master/
"""

headers = {
    'Accept' : 'application/rdf+xml'
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
    for uri in uris:
        request = Request()
        response = request.get(uri, headers=headers)
        print (response.headers.get('content-type'))
        #print request


if __name__ == '__main__':
    import time
    start = time.time()

    main()

    end = time.time()
    print (end - start)
