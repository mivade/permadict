import pytest
from permadict import Permadict


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
