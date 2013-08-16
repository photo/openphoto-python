Trovebox Python Testing
=======================

###Unit Tests

The unit tests mock out all HTTP requests, and verify that the various
components of the library are operating correctly.

They run very quickly and don't require any external test hosts.

<a name="requirements"></a>
#### Requirements
 * mock >= 1.0.0
 * httpretty >= 0.6.1
 * ddt >= 0.3.0
 * tox (optional)

#### Running the Unit Tests

    python -m unittest discover tests/unit

To run the unit tests against all supported Python versions, use ```tox```:

    tox

----------------------------------------

###Functional Tests

The functional tests check that the Trovebox python library interoperates
correctly with a real Trovebox server.

They are slow to run and rely on a stable HTTP connection to a test server.

For full details, see the [functional test README file](functional/README.markdown).
