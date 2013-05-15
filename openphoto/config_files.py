from __future__ import unicode_literals
import os
try:
    from configparser import ConfigParser # Python3
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser # Python2
try:
    import io # Python3
except ImportError:
    import StringIO as io # Python2

def get_config_path(config_file):
    config_path = os.getenv('XDG_CONFIG_HOME')
    if not config_path:
        config_path = os.path.join(os.getenv('HOME'), ".config")
    if not config_file:
        config_file = "default"
    return os.path.join(config_path, "openphoto", config_file)

def read_config(config_path):
    """
    Loads config data from the specified file path.
    If config_file doesn't exist, returns an empty authentication config for localhost.
    """
    section = "DUMMY"
    defaults = {'host': 'localhost',
                'consumerKey': '', 'consumerSecret': '',
                'token': '', 'tokenSecret':'',
                }
    # Insert an section header at the start of the config file, so ConfigParser can understand it
    buf = io.StringIO()
    buf.write('[%s]\n' % section)
    with io.open(config_path, "r") as f:
        buf.write(f.read())

    buf.seek(0, os.SEEK_SET)
    parser = ConfigParser()
    parser.optionxform = str # Case-sensitive options
    try:
        parser.read_file(buf) # Python3
    except AttributeError:
        parser.readfp(buf) # Python2

    # Trim quotes
    config = parser.items(section)
    config = [(item[0].replace('"', ''), item[1].replace('"', '')) for item in config]
    config = [(item[0].replace("'", ""), item[1].replace("'", "")) for item in config]
    config = dict(config)

    # Apply defaults
    for key in defaults:
        if key not in config:
            config[key] = defaults[key]

    return config
