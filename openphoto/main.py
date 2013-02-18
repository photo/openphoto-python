#!/usr/bin/env python
import os
import sys
import string
import urllib
from optparse import OptionParser

try:
    import simplejson as json
except:
    import json

from openphoto import OpenPhoto

def get_default_config_path():
    config_path = os.getenv('XDG_CONFIG_HOME')
    if not config_path:
        config_path = os.path.join(os.getenv('HOME'), ".config")
    return os.path.join(config_path, "openphoto", "config")

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
                      help="Path to OpenPhoto config file")
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

    if not options.config_file:
        options.config_file = get_default_config_path()
    if options.verbose:
        print "Using config from '%s'" % options.config_file
    config = read_config(options.config_file)

    # Override host if given on the commandline
    if options.host:
        config['host'] = options.host

    client = OpenPhoto(config['host'], config['consumerKey'], config['consumerSecret'],
                       config['token'], config['tokenSecret'])

    if options.method == "GET":
        result = client.get(options.endpoint, params)
    else:
        result = client.post(options.endpoint, params)

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

if __name__ == "__main__":
    main()
