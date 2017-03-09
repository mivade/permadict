from tempfile import gettempdir
import os
import os.path as osp
import sqlite3
import pytest
from permadict import Permadict


@pytest.fixture
def db_filename():
    filename = osp.join(gettempdir(), "database.sqlite")
    yield filename
    try:
        os.remove(filename)
    except:
        pass


def test_create():
    Permadict()
    Permadict(key="value", otherkey=1)
    Permadict("test.sqlite")


def test_len():
    d = Permadict(thing=1, other=2)
    assert len(d) is 2


def test_set_and_get():
    d = Permadict()
    d["key"] = "value"
    assert d["key"] == "value"

    with pytest.raises(KeyError):
        print(d["nosuchkey"])


def test_keys():
    d = Permadict(key="value")
    assert len(list(d.keys())) is 1
    assert list(d.keys()) == ["key"]


def test_in():
    d = Permadict(key="value")
    assert "key" in d
    assert "nope" not in d


def test_iterator():
    d = Permadict(one=1, two=2)
    x = [d[key] for key in d]
    assert len(x) is 2
    assert x == [1, 2]


def test_items():
    items = dict(a=1, b=2, c=3)
    d = Permadict(**items)
    for key, value in d.items():
        assert key in items
        assert key in d
        assert items[key] == d[key]


def test_context(db_filename):
    with Permadict(db_filename) as d:
        d["key"] = "value"

    with pytest.raises(sqlite3.ProgrammingError):
        d["key"]

    with Permadict(db_filename) as d:
        assert d["key"] == "value"
