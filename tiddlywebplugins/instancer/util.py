import sys
import os

import urlparse

from urllib import quote
from urllib2 import urlopen, URLError

from tiddlyweb.model.bag import Bag
from tiddlyweb.store import Store
from tiddlyweb.util import write_utf8_file, std_error_message

from tiddlywebplugins.instancer import Instance

from tiddlywebplugins.twimport import recipe_to_urls, url_to_tiddler

try:
    from pkg_resources import resource_filename
except ImportError:
    from tiddlywebplugins.utils import resource_filename


def spawn(instance_path, init_config, instance_module):
    """
    convenience wrapper for instance-creation scripts
    """
    # extend module search path for access to local tiddlywebconfig.py
    sys.path.insert(0, os.getcwd())
    from tiddlyweb.util import merge_config
    from tiddlyweb.config import config
    merge_config(config, init_config)

    package_name = instance_module.__name__.rsplit(".", 1)[0]
    instance = Instance(instance_path, config, instance_module.instance_config)
    instance.spawn(instance_module.store_structure)
    instance.update_store()


def get_tiddler_locations(store_contents, package_name):
    """
    returns instance_tiddlers structure using tiddler paths from within the
    package if available

    store_structure is a dictionary listing tiddler URIs per bag

    packaged tiddlers must be listed in <package>/resources/tiddlers.index
    """
    raise TypeError('we no do this')


def cache_tiddlers(package_name):
    """
    creates local cache of instance tiddlers to be included in distribution

    reads store_contents from <package>.instance

    tiddler files are stored in <package>/resources
    """
    instance_module = __import__("%s.instance" % package_name, None, None,
        ["instance"]) # XXX: unnecessarily convoluted and constraining!?
    store_contents = instance_module.store_contents

    target_store = Store('tiddlywebplugins.pkgstore',
            {'package': package_name, 'read_only': False}, {})

    sources = {}
    for bag, uris in store_contents.items():
        sources[bag] = []
        for uri in uris:
            if uri.endswith(".recipe"):
                urls = recipe_to_urls(uri)
                sources[bag].extend(urls)
            else:
                sources[bag].append(uri)

    for bag_name, uris in sources.items():
        bag = Bag(bag_name)
        target_store.put(bag)

        for uri in uris:
            std_error_message("retrieving %s" % uri)
            tiddler = url_to_tiddler(uri)
            tiddler.bag = bag.name
            target_store.put(tiddler)
