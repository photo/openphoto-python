Tests for the Open Photo API / Python Library
=======================
#### OpenPhoto, a photo service for the masses

----------------------------------------
<a name="requirements"></a>
### Requirements
A computer, Python 2.7 and an empty OpenPhoto instance.

---------------------------------------
<a name="setup"></a>
### Setting up

Create a tests/tokens.py file containing the following:

    # tests/tokens.py
    consumer_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    consumer_secret = "xxxxxxxxxx"
    token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    token_secret = "xxxxxxxxxx"
    host = "your_hostname"

Make sure this is an empty test server, **not a production OpenPhoto server!!!**

---------------------------------------
<a name="running"></a>
### Running the tests

    cd /path/to/openphoto-python
    python -m unittest discover -c

The "-c" lets you stop the tests gracefully with \[CTRL\]-c.

The easiest way to run a subset of the tests is with nose:

    cd /path/to/openphoto-python
    nosetests -v -s --nologcapture tests/test_albums.py:TestAlbums.test_view

All HTTP requests and responses are recorded in the file "tests.log".

---------------------------------------
<a name="test_details"></a>
### Test Details

These tests are intended to verify the Python library. They don't provide comprehensive testing of the OpenPhoto API, there are PHP unit tests for that.

Each test class is run as follows:

**SetUpClass:**

Check that the server is empty

**SetUp:**

Ensure there are:

 * Three test photos
 * A single test tag applied to each
 * A single album containing all three photos

**TearDownClass:**

Remove all photos, tags and albums

### Testing old servers

By default, all currently supported API versions will be tested.
It's useful to test servers that only support older API versions.
To restrict the testing to a specific maximum API version, use the
``OPENPHOTO_TEST_SERVER_API`` environment variable.

For example, to restrict testing to APIv1 and APIv2:

    export OPENPHOTO_TEST_SERVER_API=2

