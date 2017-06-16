import mongomock
import pytest

from mongofollow import mongofollow


@pytest.fixture
def clean_collection():
    collection = mongomock.MongoClient().test.test
    collection.drop()
    return collection


@pytest.fixture
def collection_range100(clean_collection):
    for i in range(100):
        clean_collection.insert({"i": i})
    return clean_collection


def test_inserted(collection_range100):
    assert collection_range100.count() == 100
    assert set(range(100)) == set(collection_range100.distinct("i"))


def test_stream(clean_collection):
    assert clean_collection.count() == 0
    clean_collection.insert({"i": 0})
    for i, doc in zip(range(10), mongofollow(clean_collection)):
        print(i, doc)
        j = doc["i"]
        assert i == j
        clean_collection.insert({"i": i + 1})


@pytest.mark.xfail(reason="todo", strict=True)
def test_number(collection_range100):
    for i, doc in zip(range(50, 100),
                      mongofollow(collection_range100, number=50)):
        j = doc["i"]
        assert i == j
