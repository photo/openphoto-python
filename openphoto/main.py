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

def get_config_path(config_file):
    config_path = os.getenv('XDG_CONFIG_HOME')
    if not config_path:
        config_path = os.path.join(os.getenv('HOME'), ".config")
    if not config_file:
        config_file = "default"
    return os.path.join(config_path, "openphoto", config_file)

def read_config(config_file):
    """
    Loads config data from the specified file.
    If config_file doesn't exist, returns an empty authentication config for localhost.
    """
    config = {'host': 'localhost',
              'consumerKey': '', 'consumerSecret': '',
              'token': '', 'tokenSecret':'',
              }

    if not os.path.isfile(config_file):
        print "Config file '%s' doesn't exist - authentication won't be used" % config_file
        return config

    for line_number, line in enumerate(open(config_file)):
        line = line.split('#')[0].strip() # Remove comments and surrounding whitespace
        if line:
            try:
                var,val = line.rsplit("=",1)
                config[var.strip().strip('"')] = val.strip().strip('"') # Remove whitespace and quotes
            except:
                print "WARNING: could not parse line %d: '%s'" % (line_number, line)
    return config

#################################################################

def main(args=sys.argv[1:]):
    parser = OptionParser()
    parser.add_option('-H', '--host', action='store', type='string', dest='host',
                      help="Hostname of the OpenPhoto install")
    parser.add_option('-c', '--config', action='store', type='string', dest='config_file',
                      help="Configuration file to use")
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

    config_path = get_config_path(options.config_file)
    config = read_config(config_path)
    if options.verbose:
        print "Using config from '%s'" % config_path

    # Override host if given on the commandline
    if options.host:
        config['host'] = options.host

    client = OpenPhoto(config['host'], config['consumerKey'], config['consumerSecret'],
                       config['token'], config['tokenSecret'])

    if options.method == "GET":
        result = client.get(options.endpoint, process_response=False, **params)
    else:
        params, files = extract_files(params)
        result = client.post(options.endpoint, process_response=False, files=files, **params)

    if options.verbose:
        print "==========\nMethod: %s\nHost: %s\nEndpoint: %s" % (options.method, config['host'], options.endpoint)
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
