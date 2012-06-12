# (c)2012 Rackspace Hosting

PLUGIN_DIR="plugins"

# we need sys to import modules by name
import sys
import httplib2
import json
import re

"""
list = Extensions(endpoint, auth=false)
"""
class Extensions:

    def load_extensions(self, endpoint, auth=False):
        # TODO: add auth handling and token-getting
        self.extensions = []
        h = httplib2.Http()
        response, rawcontent = h.request(endpoint + "/extensions/")
        
        # convert the payload to an object
        content = json.loads(rawcontent)
        
        # try to load a plugin for each extension
        for item in content['extensions']:
            modname = self._modname(item['alias'])
            # attempt to load plugin
            self.extensions.append(self._get_extension(modname))

    """
    _get_extension(classname) - given an extension named "classname", attempts to
    load a module from the plugins directory with that name, then instantiates
    a class with that name, passing itself as a parameter
    """
    def _get_extension(self, classname):
        name = PLUGIN_DIR + '.' + classname.encode()
        try:
            __import__(name)
            classobj = getattr(sys.modules[name], classname)
            self.extensions.append(classobj(self))
            #print "succeeded"
        except:
            #print "failed"
            return

    """
    _modname(alias) - converts a module alias to a valid Python module name
    """
    def _modname(self, alias):
        temp = re.sub('[^a-zA-Z0-9_]', '_', alias)
        return temp.lower()