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

To use the library you need to first ``import openphoto``, then instantiate an instance of the class and start making calls.

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

When using the command line tools, you'll want to export your secrets to the environment.
We suggest putting them in a file and sourcing it prior to running `openphoto` commands.
<a href="#credentials">Click here for instructions on getting credentials</a>.

    # env.sh
    export consumerKey=your_consumer_key
    export consumerSecret=your_consumer_secret
    export token=your_access_token
    export tokenSecret=your_access_token_secret

You'll need to source that file once for each terminal session.
    
    source env.sh

These are the options you can pass to the shell program.

    -h # display help text
    -H hostname # default=localhost
    -e endpoint # default=/photos/list.json
    -X method # default=GET
    -F params # i.e. -F 'title=my title' -F 'tags=mytag1,mytag1'
    -p # pretty print the json
    -v # verbose output
    --encode # base 64 encode the photo

Now you can run commands to the OpenPhoto API from your shell!

    openphoto -H current.openphoto.me -p -e /photo/62/view.json -F 'returnSizes=20x20'
    {
      "message" : "Photo 62",
      "code" : 200,
      "result" : {
        "tags" : [
          
        ],
        "id" : "62",
        "appId" : "current.openphoto.me",
        "pathBase" : "\/base\/201108\/1312956581-opmeqViHrD.jpg",
        "dateUploadedMonth" : "08",
        "dateTakenMonth" : "08",
        "exifCameraMake" : "",
        "dateTaken" : "1312956581",
        "title" : "Tomorrowland Main Stage 2011",
        "height" : "968",
        "description" : "",
        "creativeCommons" : "BY-NC",
        "dateTakenYear" : "2011",
        "dateUploadedDay" : "09",
        "longitude" : "4",
        "host" : "opmecurrent.s3.amazonaws.com",
        "hash" : "0455675a8c42148238b81ed1d8db655c45ae055a",
        "status" : "1",
        "width" : "1296",
        "dateTakenDay" : "09",
        "permission" : "1",
        "pathOriginal" : "\/original\/201108\/1312956581-opmeqViHrD.jpg",
        "size" : "325",
        "dateUploadedYear" : "2011",
        "views" : "0",
        "latitude" : "50.8333",
        "dateUploaded" : "1312956583",
        "exifCameraModel" : "",
        "Name" : "62",
        "path20x20" : "http:\/\/current.openphoto.me\/photo\/62\/create\/ceb90\/20x20.jpg"
      }
    }

<a name="credentials"></a>
#### Getting your credentials

You can get your credentals by clicking on the arrow next to your email address once you're logged into your site and then clicking on settings.
If you don't have any credentials then you can create one for yourself by going to `/v1/oauth/flow`.
Once completed go back to the settings page and you should see the credential you just created

