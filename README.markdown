Open Photo API / Python Library
=======================
#### OpenPhoto, a photo service for the masses

----------------------------------------
<a name="install"></a>
### Installation
    python setup.py install

----------------------------------------

<a name="python"></a>
### How to use the library

To use the library you need to first ``import openphoto`` then instantiate an instance of the class and start making calls.

You can use the library in one of two ways:

 * Direct GET/POST calls to the server
 * Access via Python classes/methods

<a name="get_post"></a>
### Direct GET/POST:

    from openphoto import OpenPhoto
    client = OpenPhoto(host, consumerKey, consumerSecret, token, tokenSecret)
    resp = client.get("/photos/list.json")
    resp = client.post("/photo/62/update.json", tags=["tag1", "tag2"])

<a name="python_classes"></a>
### Python classes/methods

    from openphoto import OpenPhoto
    client = OpenPhoto(host, consumerKey, consumerSecret, token, tokenSecret)
    photos = client.photos.list()
    photos[0].update(tags=["tag1", "tag2"])
    print photos[0].tags

The OpenPhoto Python class hierarchy mirrors the [OpenPhoto API](http://theopenphotoproject.org/documentation) endpoint layout. For example, the calls in the example above use the following API endpoints:

* client.photos.list() -> /photos/list.json
* photos[0].update() -> /photo/&lt;id&gt;/update.json

----------------------------------------

<a name="cli"></a>
### Using from the command line

When using the command line tool, you'll want to export your authentication credentials to the environment. 
The command line tool will look for the following config file in ~/.config/openphoto/default
(the -c switch lets you specify a different config file):

    # ~/.config/openphoto/default
    host = your.host.com
    consumerKey = your_consumer_key
    consumerSecret = your_consumer_secret
    token = your_access_token
    tokenSecret = your_access_token_secret

<a href="#credentials">Click here for instructions on getting credentials</a>.

These are the options you can pass to the shell program:

    -h             # Display help text
    -c config_file # Either the name of a config file in ~/.config/openphoto/ or a full path to a config file
    -H hostname    # Overrides config_file for unauthenticated API calls [default=localhost]
    -e endpoint    # [default=/photos/list.json]
    -X method      # [default=GET]
    -F params      # e.g. -F 'title=my title' -F 'tags=mytag1,mytag2'
    -p             # Pretty print the json
    -v             # Verbose output

You can run commands to the OpenPhoto API from your shell!

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
    openphoto -H current.openphoto.me -p -e /photo/62/view.json -F 'returnSizes=20x20'
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

<a name="credentials"></a>
#### Getting your credentials

You can get your credentals by clicking on the arrow next to your email address once you're logged into your site and then clicking on settings.
If you don't have any credentials then you can create one for yourself using the "Create a new app" button.
