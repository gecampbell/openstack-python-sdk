# (c)2012 Rackspace Hosting

"""
rax_kskey: extension to handle the Rackspace API key extension to Keystone
"""
class rax_kskey:

    def __init__(self, parent):
        # save the parent object
        self.parent = parent
        self.username = parent.secret['username']
        self.apiKey = parent.secret['apiKey']
        self.tenantName = parent.secret['tenantName']
        parent.credentials = self._rax_credentials

    def _rax_credentials(self):
        """Authenticate against the Rackspace auth service."""
        body = {"auth": {
            "RAX-KSKEY:apiKeyCredentials": {
            "username": self.username,
            "apiKey": self.apiKey,
            "tenantName": self.tenantName}}}
        return body