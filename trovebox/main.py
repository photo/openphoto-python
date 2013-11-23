#!/usr/bin/env python
"""
main.py : Trovebox Console Script
"""
import os
import sys
import json
from optparse import OptionParser

import trovebox

CONFIG_ERROR = """
You must create a configuration file with the following contents:
    host = your.host.com
    consumerKey = your_consumer_key
    consumerSecret = your_consumer_secret
    token = your_access_token
    tokenSecret = your_access_token_secret

To get your credentials:
 * Log into your Trovebox site
 * Click the arrow on the top-right and select 'Settings'.
 * Click the 'Create a new app' button.
 * Click the 'View' link beside the newly created app.
"""

#################################################################

def main(args=sys.argv[1:]):
    """Run the commandline script"""
    usage = "%prog --help"
    parser = OptionParser(usage, add_help_option=False)
    parser.add_option('-c', '--config', help="Configuration file to use",
                      action='store', type='string', dest='config_file')
    parser.add_option('-h', '-H', '--host',
                      help=("Hostname of the Trovebox server "
                            "(overrides config_file)"),
                      action='store', type='string', dest='host')
    parser.add_option('-X', help="Method to use (GET or POST)",
                      action='store', type='choice', dest='method',
                      choices=('GET', 'POST'), default="GET")
    parser.add_option('-F', help="Endpoint field",
                      action='append', type='string', dest='fields')
    parser.add_option('-e', help="Endpoint to call",
                      action='store', type='string', dest='endpoint',
                      default='/photos/list.json')
    parser.add_option('-p', help="Pretty print the json",
                      action="store_true", dest="pretty", default=False)
    parser.add_option('-v', help="Verbose output",
                      action="store_true", dest="verbose", default=False)
    parser.add_option('--version', help="Display the current version",
                      action="store_true")
    parser.add_option('--help', help='show this help message',
                      action="store_true")

    options, args = parser.parse_args(args)

    if options.help:
        parser.print_help()
        return

    if options.version:
        print(trovebox.__version__)
        return

    if args:
        parser.error("Unknown argument: %s" % args)

    params = {}
    if options.fields:
        for field in options.fields:
            (key, value) = field.split('=')
            params[key] = value

    # Host option overrides config file settings
    if options.host:
        client = trovebox.Trovebox(host=options.host)
    else:
        try:
            client = trovebox.Trovebox(config_file=options.config_file)
        except IOError as error:
            print(error)
            print(CONFIG_ERROR)
            print(error)
            sys.exit(1)

    if options.method == "GET":
        result = client.get(options.endpoint, process_response=False,
                            **params)
    else:
        params, files = extract_files(params)
        result = client.post(options.endpoint, process_response=False,
                             files=files, **params)
        for file_ in files:
            files[file_].close()

    if options.verbose:
        print("==========\nMethod: %s\nHost: %s\nEndpoint: %s" %
              (options.method, client.host, options.endpoint))
        if params:
            print("Fields:")
            for key, value in params.items():
                print("  %s=%s" % (key, value))
        print("==========\n")

    if options.pretty:
        print(json.dumps(json.loads(result), sort_keys=True,
                         indent=4, separators=(',',':')))
    else:
        print(result)

def extract_files(params):
    """
    Extract filenames from the "photo" parameter so they can be uploaded,
    returning (updated_params, files).
    Uses the same technique as the Trovebox PHP commandline tool:
      * Filename can only be in the "photo" parameter
      * Filename must be prefixed with "@"
      * Filename must exist
    ...otherwise the parameter is not extracted
    """
    files = {}
    updated_params = {}
    for name in params:
        if (name == "photo" and params[name].startswith("@") and
                os.path.isfile(os.path.expanduser(params[name][1:]))):
            files[name] = open(params[name][1:], 'rb')
        else:
            updated_params[name] = params[name]

    return updated_params, files

if __name__ == "__main__": # pragma: no cover
    main()
