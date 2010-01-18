import os

from urllib2 import HTTPError, URLError

from py.test import raises

from tiddlywebplugins.instancer.sourcer import from_list


FIXTURES_DIR = "test/fixtures"
REPO_DIR = "%s/repo" % FIXTURES_DIR
REPO_URI = "file://%s" % os.path.abspath(REPO_DIR)


def test_recipe_expansion():
    uri = "%s/alpha/index.recipe" % REPO_URI
    tiddlers = from_list([uri])

    actual = [tiddler.title for tiddler in tiddlers]
    expected = ["common", "Foo", "Lorem", "foo"]
    assert actual == expected


def test_recursive_recipe_expansion():
    uri = "%s/bravo/index.recipe" % REPO_URI
    tiddlers = from_list([uri])

    actual = [tiddler.title for tiddler in tiddlers]
    expected = ["common", "Foo", "Lorem", "foo",
        "common", "Bar", "Ipsum", "BarPlugin"]
    assert actual == expected


def test_from_list():
    uris = [
        "%s/alpha/tiddlers/Foo.tid" % REPO_URI,
        "%s/alpha/tiddlers/lorem.tiddler" % REPO_URI,
        "%s/alpha/plugins/foo.js" % REPO_URI,
        "%s/alpha/index.recipe" % REPO_URI
    ]
    tiddlers = from_list(uris)

    actual = [tiddler.title for tiddler in tiddlers]
    expected = ["Foo", "Lorem", "foo", "common", "Foo", "Lorem", "foo"]
    assert actual == expected

    tiddler = tiddlers[0]
    assert tiddler.title == "Foo"
    assert tiddler.tags == ["foo", "bar baz"]
    assert tiddler.text == "lorem ipsum\nfoo\ndolor sit amet"

    tiddler = tiddlers[1]
    assert tiddler.title == "Lorem"
    assert tiddler.tags == ["foo", "bar baz"]
    assert tiddler.text == "lorem ipsum\ndolor sit amet"

    tiddler = tiddlers[2]
    assert tiddler.title == "foo"
    assert tiddler.tags == ["systemConfig"]
    assert tiddler.text == 'alert("foo");'


def test_one_tiddler():
    uri = "%s/alpha/tiddlers/lorem.tiddler" % REPO_URI
    tiddler = from_list([uri])[0]
    assert tiddler.title == "Lorem"
    assert tiddler.tags == ["foo", "bar baz"]
    assert tiddler.text == "lorem ipsum\ndolor sit amet"

    uri = "%s/alpha/tiddlers/Foo.tid" % REPO_URI
    tiddler = from_list([uri])[0]
    assert tiddler.title == "Foo"
    assert tiddler.tags == ["foo", "bar baz"]
    assert tiddler.text == "lorem ipsum\nfoo\ndolor sit amet"

    uri = "%s/alpha/plugins/foo.js" % REPO_URI
    tiddler = from_list([uri])[0]
    assert tiddler.title == "foo"
    assert tiddler.tags == ["systemConfig"]
    assert tiddler.text == 'alert("foo");'


def test_one_plugin():
    uri = "%s/alpha/plugins/foo.js" % REPO_URI
    tiddler = from_list([uri])[0]

    assert tiddler.title == "foo"
    assert tiddler.tags == ["systemConfig"]
    assert tiddler.text == 'alert("foo");'

    uri = "%s/bravo/plugins/bar.js" % REPO_URI
    tiddler = from_list([uri])[0]

    assert tiddler.title == "BarPlugin"
    assert tiddler.tags == ["foo", "bar baz", "..."]
    assert tiddler.text == 'alert("bar");'


def test_one_tid():
    uri = "%s/alpha/tiddlers/Foo.tid" % REPO_URI
    tiddler = from_list([uri])[0]

    assert tiddler.title == "Foo"
    assert tiddler.tags == ["foo", "bar baz"]
    assert tiddler.text == "lorem ipsum\nfoo\ndolor sit amet"

    uri = "%s/bravo/tiddlers/Bar.tid" % REPO_URI
    tiddler = from_list([uri])[0]

    assert tiddler.title == "Bar"
    assert tiddler.tags == ["foo", "bar baz", "..."]
    assert tiddler.text == "lorem ipsum\nbar\ndolor sit amet"

    uri = "%s/alpha/tiddlers/common.tid" % REPO_URI
    tiddler = from_list([uri])[0]

    assert tiddler.title == "common"
    assert tiddler.tags == []
    assert tiddler.text == "Alpha"

    uri = "%s/bravo/tiddlers/common.tid" % REPO_URI
    tiddler = from_list([uri])[0]

    assert tiddler.title == "common"
    assert tiddler.tags == []
    assert tiddler.text == "Bravo"


def test_another_tiddler():
    uri = "%s/alpha/tiddlers/lorem.tiddler" % REPO_URI
    tiddler = from_list([uri])[0]

    assert tiddler.title == "Lorem"
    assert tiddler.tags == ["foo", "bar baz"]
    assert tiddler.text == "lorem ipsum\ndolor sit amet"

    uri = "%s/bravo/tiddlers/ipsum.tiddler" % REPO_URI
    tiddler = from_list([uri])[0]

    assert tiddler.title == "Ipsum"
    assert tiddler.tags == ["foo", "bar baz", "..."]
    assert tiddler.text == "lorem ipsum\ndolor sit amet"
