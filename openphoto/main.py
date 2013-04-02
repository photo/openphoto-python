#!/usr/bin/env python
import os
import sys
import string
import urllib
from optparse import OptionParser

try:
    import json
except ImportError:
    import simplejson as json

from openphoto import OpenPhoto

def main(args=sys.argv[1:]):
    consumer_key = os.getenv('consumerKey')
    consumer_secret = os.getenv('consumerSecret')
    token = os.getenv('token')
    token_secret = os.getenv('tokenSecret')

    parser = OptionParser()
    parser.add_option('-H', '--host', action='store', type='string', dest='host', 
                      help="Hostname of the OpenPhoto install", default="localhost")
    parser.add_option('-X', action='store', type='choice', dest='method', choices=('GET', 'POST'),
                      help="Method to use (GET or POST)", default="GET")
    parser.add_option('-F', action='append', type='string', dest='fields',
                      help="Fields")
    parser.add_option('-e', action='store', type='string', dest='endpoint',
                      default='/photos/list.json',
                      help="Endpoint to call")
    parser.add_option('-p', action="store_true", dest="pretty", default=False,
                      help="pretty print the json")
    parser.add_option('-v', action="store_true", dest="verbose", default=False,
                      help="verbose output")
    parser.add_option('--encode', action="store_true", dest="encode", default=False)

    options, args = parser.parse_args(args)

    params = {}
    if options.fields:
        for field in options.fields:
            (key, value) = string.split(field, '=')
            params[key] = value

    client = OpenPhoto(options.host, consumer_key, consumer_secret, token, token_secret)

    if options.method == "GET":
        result = client.get(options.endpoint, process_response=False, **params)
    else:
        params, files = extract_files(params)
        result = client.post(options.endpoint, process_response=False, files=files, **params)

    if options.verbose:
        print "==========\nMethod: %s\nHost: %s\nEndpoint: %s" % (options.method, options.host, options.endpoint)
        if len( params ) > 0:
            print "Fields:"
            for kv in params.iteritems():
                print "  %s=%s" % kv
        print "==========\n"

    if options.pretty:
        print json.dumps(json.loads(result), sort_keys=True, indent=4, separators=(',',':'))
    else:
        print result

def extract_files(params):
    """
    Extract filenames from the "photo" parameter, so they can be uploaded, returning (updated_params, files).
    Uses the same technique as openphoto-php:
      * Filename can only be in the "photo" parameter
      * Filename must be prefixed with "@"
      * Filename must exist
    ...otherwise the parameter is not extracted
    """
    files = {}
    updated_params = {}
    for name in params:
        if name == "photo" and params[name].startswith("@") and os.path.isfile(os.path.expanduser(params[name][1:])):
            files[name] = params[name][1:]
        else:
            updated_params[name] = params[name]

    return updated_params, files

if __name__ == "__main__":
    main()
