"""
auth.py : OAuth Config File Parser
"""
from __future__ import unicode_literals
import os
try:
    from configparser import ConfigParser # Python3
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser # Python2
try:
    import io # Python3
except ImportError: # pragma: no cover
    import StringIO as io # Python2

class Auth(object):
    """OAuth secrets"""
    def __init__(self, config_file, host,
                 consumer_key, consumer_secret,
                 token, token_secret):
        if host is None:
            self.config_path = get_config_path(config_file)
            config = read_config(self.config_path)
            self.host = config['host']
            self.consumer_key = config['consumerKey']
            self.consumer_secret = config['consumerSecret']
            self.token = config['token']
            self.token_secret = config['tokenSecret']
        else:
            self.config_path = None
            self.host = host
            self.consumer_key = consumer_key
            self.consumer_secret = consumer_secret
            self.token = token
            self.token_secret = token_secret

        if host is not None and config_file is not None:
            raise ValueError("Cannot specify both host and config_file")

def get_config_path(config_file):
    """
    Given the name of a config file, returns the full path
    """
    config_path = os.getenv('XDG_CONFIG_HOME')
    if not config_path:
        config_path = os.path.join(os.getenv('HOME'), ".config")
    if not config_file:
        config_file = "default"
    return os.path.join(config_path, "trovebox", config_file)

def read_config(config_path):
    """
    Loads config data from the specified file path.
    If config_file doesn't exist, returns an empty authentication config
    for localhost.
    """
    section = "DUMMY"
    defaults = {'host': 'localhost',
                'consumerKey': '', 'consumerSecret': '',
                'token': '', 'tokenSecret':'',
                }
    # Insert an section header at the start of the config file,
    # so ConfigParser can understand it
    buf = io.StringIO()
    buf.write('[%s]\n' % section)
    with io.open(config_path, "r") as conf:
        buf.write(conf.read())

    buf.seek(0, os.SEEK_SET)
    parser = ConfigParser()
    parser.optionxform = str # Case-sensitive options
    try:
        parser.read_file(buf) # Python3
    except AttributeError:
        parser.readfp(buf) # Python2

    # Trim quotes
    config = parser.items(section)
    config = [(item[0].replace('"', ''), item[1].replace('"', ''))
              for item in config]
    config = [(item[0].replace("'", ""), item[1].replace("'", ""))
              for item in config]
    config = dict(config)

    # Apply defaults
    for key in defaults:
        if key not in config:
            config[key] = defaults[key]

    return config
