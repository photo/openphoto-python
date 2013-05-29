Open Photo API / Python Library
=======================
#### OpenPhoto, a photo service for the masses
[![Build Status](https://api.travis-ci.org/photo/openphoto-python.png)](https://travis-ci.org/photo/openphoto-python)

----------------------------------------
<a name="install"></a>
### Installation
    python setup.py install

----------------------------------------
<a name="credentials"></a>
### Credentials

For full access to your photos, you need to create the following config file in ``~/.config/openphoto/default``

    # ~/.config/openphoto/default
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

----------------------------------------
<a name="python"></a>
### How to use the library

You can use the library in one of two ways:

 * Direct GET/POST calls to the server
 * Access via Python classes/methods

<a name="get_post"></a>
#### Direct GET/POST:

    from openphoto import OpenPhoto
    client = OpenPhoto()
    resp = client.get("/photos/list.json")
    resp = client.post("/photo/62/update.json", tags=["tag1", "tag2"])

<a name="python_classes"></a>
#### Python classes/methods

    from openphoto import OpenPhoto
    client = OpenPhoto()
    photos = client.photos.list()
    photos[0].update(tags=["tag1", "tag2"])
    print photos[0].tags

The OpenPhoto Python class hierarchy mirrors the [OpenPhoto API](http://theopenphotoproject.org/documentation) endpoint layout. For example, the calls in the example above use the following API endpoints:

* ``client.photos.list() -> /photos/list.json``
* ``photos[0].update()   -> /photo/<id>/update.json``

<a name="api_versioning"></a>
### API Versioning

It may be useful to lock your application to a particular version of the OpenPhoto API.
This ensures that future API updates won't cause unexpected breakages.

To do this, add the optional ```api_version``` parameter when creating the client object:

    from openphoto import OpenPhoto
    client = OpenPhoto(api_version=2)

----------------------------------------

<a name="cli"></a>
### Using from the command line

You can run commands to the OpenPhoto API from your shell!

These are the options you can pass to the shell program:

    --help         # Display help text
    -c config_file # Either the name of a config file in ~/.config/openphoto/ or a full path to a config file
    -h hostname    # Overrides config_file for unauthenticated API calls
    -e endpoint    # [default=/photos/list.json]
    -X method      # [default=GET]
    -F params      # e.g. -F 'title=my title' -F 'tags=mytag1,mytag2'
    -p             # Pretty print the json
    -v             # Verbose output

<a name="cli-examples"></a>
#### Command line examples

    # Upload a public photo to the host specified in ~/.config/openphoto/default
    openphoto -p -X POST -e /photo/upload.json -F 'photo=@/path/to/photo/jpg' -F 'permission=1'
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
    
    # Get a thumbnail URL from current.openphoto.me (unauthenticated access)
    openphoto -h current.openphoto.me -p -e /photo/62/view.json -F 'returnSizes=20x20'
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
            "path20x20":"http://current.openphoto.me/photo/62/create/36c0a/20x20.jpg",
            "pathBase":"http://awesomeness.openphoto.me/base/201203/7ae997-Boracay-Philippines-007.jpg",
            "permission":"1",
            "photo20x20":[
                "http://current.openphoto.me/photo/62/create/36c0a/20x20.jpg",
                13,
                20
            ],
            ...
            ...
        }
    }    
