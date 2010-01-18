"""
utility module for retrieving TiddlerS from Cook-style TiddlyWiki resources

supports .tiddler, .tid, .js and .recipe files
"""

from tiddlywebplugins.twimport import recipe_to_urls, url_to_tiddler


def from_list(uris):
    """
    generates collection of TiddlerS from a list of URIs

    supports .tiddler, .tid, .js and .recipe files
    """
    sources = []
    for uri in uris:
        if uri.endswith(".recipe"):
            urls = recipe_to_urls(uri)
            sources.extend(urls)
        else:
            sources.append(uri)

    return [url_to_tiddler(uri) for uri in sources]
