=======================
Trovebox Python Library
=======================
(Previously known as openphoto-python)

.. image:: https://api.travis-ci.org/photo/openphoto-python.png
   :alt: Build Status
   :target: https://travis-ci.org/photo/openphoto-python

.. image:: https://pypip.in/v/trovebox/badge.png
   :alt: Python Package Index (PyPI)
   :target: https://pypi.python.org/pypi/trovebox

This library works with any Trovebox server, either
`self-hosted <https://github.com/photo>`__, or using the hosted service at
`trovebox.com <http://trovebox.com>`__.
It provides full access to your photos and metadata, via a simple
Pythonic API.

Installation
============
::

    pip install trovebox

Documentation
=============
See the `Trovebox API Documentation <https://trovebox.com/documentation>`__
for full API documentation, including Python examples.

All development takes place at the `openphoto-python GitHub site <https://github.com/photo/openphoto-python>`__.

Credentials
===========
For full access to your photos, you need to create the following config
file in ``~/.config/trovebox/default``::

    # ~/.config/trovebox/default
    host = your.host.com
    consumerKey = your_consumer_key
    consumerSecret = your_consumer_secret
    token = your_access_token
    tokenSecret = your_access_token_secret

The ``config_file`` switch lets you specify a different config file.

To get your credentials:

* Log into your Trovebox site
* Click the arrow on the top-right and select 'Settings'
* Click the 'Create a new app' button
* Click the 'View' link beside the newly created app

Using the library
=================
::

    from trovebox import Trovebox
    client = Trovebox()
    photos = client.photos.list()
    photos[0].update(tags=["tag1", "tag2"])
    print(photos[0].tags)

The Trovebox Python class hierarchy mirrors the
`Trovebox API <https://trovebox.com/documentation>`__ endpoint layout.
For example, the calls in the example above use the following API endpoints:

* ``client.photos.list() -> /photos/list.json``
* ``photos[0].update()   -> /photo/<id>/update.json``

You can also access the API at a lower level using GET/POST methods::

    resp = client.get("/photos/list.json")
    resp = client.post("/photo/62/update.json", tags=["tag1", "tag2"])

API Versioning
==============
It may be useful to lock your application to a particular version of the Trovebox API.
This ensures that future API updates won't cause unexpected breakages.

To do this, add the optional ``api_version`` parameter when creating the client object::

    from trovebox import Trovebox
    client = Trovebox(api_version=2)

Commandline Tool
================
You can run commands to the Trovebox API from your shell!

These are the options you can pass to the shell program::

    --help         # Display help text
    -c config_file # Either the name of a config file in ~/.config/trovebox/ or a full path to a config file
    -h hostname    # Overrides config_file for unauthenticated API calls
    -e endpoint    # [default=/photos/list.json]
    -X method      # [default=GET]
    -F params      # e.g. -F 'title=my title' -F 'tags=mytag1,mytag2'
    -p             # Pretty print the json
    -v             # Verbose output
    --version      # Display the current version information

Commandline Examples
--------------------
Upload a public photo to the host specified in ```~/.config/trovebox/default```::

    trovebox -p -X POST -e /photo/upload.json -F 'photo=@/path/to/photo/jpg' -F 'permission=1'
    {
        "code":201,
        "message":"Photo 1eo uploaded successfully",
        "result":{
            "actor":"user@example.com",
            "albums":[],
            ...
            ...
        }
    }

Get a thumbnail URL from current.trovebox.com (unauthenticated access)::

    trovebox -h current.trovebox.com -p -e /photo/62/view.json -F 'returnSizes=20x20'
    {
        "code":200,
        "message":"Photo 62",
        "result":{
            "actor":"",
            "albums":[
                "1"
            ],
            ...
            ...
            "path20x20":"http://current.trovebox.com/photo/62/create/36c0a/20x20.jpg",
            "pathBase":"http://awesomeness.trovebox.com/base/201203/7ae997-Boracay-Philippines-007.jpg",
            "permission":"1",
            "photo20x20":[
                "http://current.trovebox.com/photo/62/create/36c0a/20x20.jpg",
                13,
                20
            ],
            ...
            ...
        }
    }
