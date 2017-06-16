"""Tail any mongodb collection"""

from bson import ObjectId

__version__ = "0.3.1"


def fetch(collection, filter, last_oid_generation_time=None):
    if last_oid_generation_time is not None:
        last_oid = ObjectId.from_datetime(last_oid_generation_time)
        filter.update({"_id": {"$gte": last_oid}})
    return collection.find(filter)


def filter_duplicates(cursor, ids):
    for doc in cursor:
        if doc["_id"] not in ids:
            yield doc


def mongofollow(collection, filter=None):
    if filter is None:
        filter = {}
    last_oid_generation_time = None
    last_oids = {}
    while True:
        cursor = fetch(collection, filter, last_oid_generation_time)
        for doc in filter_duplicates(cursor, last_oids):
            oid = doc["_id"]
            last_oid_generation_time = doc["_id"].generation_time
            last_oids = {oid for oid in last_oids if
                         oid.generation_time ==last_oid_generation_time}
            last_oids.add(oid)
            yield doc
