import os

from pymongo import MongoClient
import pytest

from mongofollow import mongofollow


@pytest.fixture
def clean_collection():
    uri = os.environ.get("MONGO_HOST", "mongodb://localhost/test")
    collection = MongoClient(uri).test.test
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
    i = 0
    for doc in mongofollow(clean_collection):
        assert i == doc["i"]
        i+= 1
        clean_collection.insert({"i": doc["i"] + 1})
        if i >= 20:
            break
    # for i, doc in zip(range(10), mongofollow(clean_collection)):
        # print(i, doc)
        # j = doc["i"]
        # assert i == j
        # clean_collection.insert({"i": i + 1})
