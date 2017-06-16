import mongomock
import pytest


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
