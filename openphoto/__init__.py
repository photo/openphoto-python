import oauth2 as oauth
import urlparse
import urllib
import httplib2
import types


class OpenPhoto(object):
    """ Client library for OpenPhoto """

    def __init__(self, host, consumer_key='', consumer_secret='',
                 token='', token_secret=''):
        self.host = host
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.token = token
        self.token_secret = token_secret

    def get(self, endpoint, params={}):
        url = urlparse.urlunparse(('http', self.host, endpoint, '',
                                   urllib.urlencode(params), ''))
        if self.consumer_key:
            consumer = oauth.Consumer(self.consumer_key, self.consumer_secret)
            token = oauth.Token(self.token, self.token_secret)

            client = oauth.Client(consumer, token)

        else:
            client = httplib2.Http()

        headers, content = client.request(url, "GET")
        return content

    def post(self, endpoint, params={}):
        url = urlparse.urlunparse(('http', self.host, endpoint, '', '', ''))

        if self.consumer_key:
            consumer = oauth.Consumer(self.consumer_key, self.consumer_secret)
            token = oauth.Token(self.token, self.token_secret)

            # ensure utf-8 encoding for all values.
            params = dict([(k, v.encode('utf-8')
                            if type(v) is types.UnicodeType else v)
                           for (k, v) in params.items()])

            client = oauth.Client(consumer, token)
            body = urllib.urlencode(params)
            headers, content = client.request(url, "POST", body)

            return content
