#!/usr/bin/env python
import os
import sys
import string
import json
from optparse import OptionParser

from openphoto import OpenPhoto

#################################################################

def main(args=sys.argv[1:]):
    usage = "%prog --help"
    parser = OptionParser(usage, add_help_option=False)
    parser.add_option('-c', '--config', action='store', type='string', dest='config_file',
                      help="Configuration file to use")
    parser.add_option('-h', '-H', '--host', action='store', type='string', dest='host',
                      help="Hostname of the OpenPhoto server (overrides config_file)")
    parser.add_option('-X', action='store', type='choice', dest='method', choices=('GET', 'POST'),
                      help="Method to use (GET or POST)", default="GET")
    parser.add_option('-F', action='append', type='string', dest='fields',
                      help="Fields")
    parser.add_option('-e', action='store', type='string', dest='endpoint',
                      default='/photos/list.json',
                      help="Endpoint to call")
    parser.add_option('-p', action="store_true", dest="pretty", default=False,
                      help="Pretty print the json")
    parser.add_option('-v', action="store_true", dest="verbose", default=False,
                      help="Verbose output")
    parser.add_option('--help', action="store_true", help='show this help message')

    options, args = parser.parse_args(args)

    if options.help:
        parser.print_help()
        return

    if args:
        parser.error("Unknown argument: %s" % args)

    params = {}
    if options.fields:
        for field in options.fields:
            (key, value) = string.split(field, '=')
            params[key] = value

    # Host option overrides config file settings
    if options.host:
        client = OpenPhoto(host=options.host)
    else:
        try:
            client = OpenPhoto(config_file=options.config_file)
        except IOError as error:
            print(error)
            print()
            print("You must create a configuration file with the following contents:")
            print("    host = your.host.com")
            print("    consumerKey = your_consumer_key")
            print("    consumerSecret = your_consumer_secret")
            print("    token = your_access_token")
            print("    tokenSecret = your_access_token_secret")
            print()
            print("To get your credentials:")
            print(" * Log into your Trovebox site")
            print(" * Click the arrow on the top-right and select 'Settings'.")
            print(" * Click the 'Create a new app' button.")
            print(" * Click the 'View' link beside the newly created app.")
            print()
            print(error)
            sys.exit(1)

    if options.method == "GET":
        result = client.get(options.endpoint, process_response=False, **params)
    else:
        params, files = extract_files(params)
        result = client.post(options.endpoint, process_response=False, files=files, **params)

    if options.verbose:
        print("==========\nMethod: %s\nHost: %s\nEndpoint: %s" % (options.method, config['host'], options.endpoint))
        if len( params ) > 0:
            print("Fields:")
            for kv in params.items():
                print("  %s=%s" % kv)
        print("==========\n")

    if options.pretty:
        print(json.dumps(json.loads(result), sort_keys=True, indent=4, separators=(',',':')))
    else:
        print(result)

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
            files[name] = open(params[name][1:], 'rb')
        else:
            updated_params[name] = params[name]

    return updated_params, files

if __name__ == "__main__":
    main()
