# (c)2012 Rackspace Hosting

# we need to handle extensions in this class
from extensions import Extensions

# general modules required
import time
import httplib2
import json

"""
The Identity class manages Keystone connections and extensions. To authenticate 
one's self with a particular service:

auth = Identity(endpoint, secret)
(token, catalog) = auth.authenticate()

It manages persistent tokens and only re-authenticates against the endpoint when
the token has expired.

endpoint - a URL of an identity endpoint
secret - a dictionary containing authentication information specific to the endpoint
    This will usually be {username: "me", password: "something"} but may be
    revised based on the extensions installed at the endpoint. For example, Rackspace
    will need {username: "me", tenant: ID, APIkey: "something"}
"""
class Identity(Extensions):

    def __init__(self, endpoint, secret):
        self.endpoint = endpoint
        self.secret = secret
        
        # note that we don't actually authenticate at this time
        # that only happens when we retrieve a token
        self.token = None
        self.catalog = None
        self.expiration = -1
        
        # set default methods
        self.credentials = self._v2_auth

        # load any extensions (no auth for Identity)
        # note that this has to happen LAST, since
        self.load_extensions(endpoint)

    def _v2_auth(self, url):
        """ Authenticate against a v2.0 auth service """
        return {"auth": {
            "passwordCredentials": {"username": self.user,
                                    "password": self.secret}}}

    def get_token(self):
        """ returns a token and service catalog, re-authenticating if necessary """
        if time.time() > self.expiration:
            # need to re-authenticate and get a new token and catalog
            self._authenticate()
        
        return self.token, self.catalog

    def _authenticate(self):
        """ authenticate with the defined endpoint """
        url = self.endpoint + "/tokens"
        h = httplib2.Http()
        response, rawcontent = h.request(
                url, 
                method="POST",
                headers={ "Content-Type":"application/json" },
                body=json.dumps(self.credentials()))
        content = json.loads(rawcontent)
        self.token = content['access']['token']['id']
        self.expiration = content['access']['token']['expires']
        self.catalog = content['access']['serviceCatalog']

