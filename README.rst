Mongofollow
###########

`mongofollow` is a simple generator yielding documents inserted in a
collection.

Installation
============

You can install it with pip::

    $ pip install mongofollow

How to use
==========

.. code-block:: python

    from mongofollow import mongofollow
    from pymongo import MongoClient

    collection = MongoClient("mongodb://SOME_URI").db_name.collection_name

    for document in mongofollow(collection):
        print(document)


This snippet will begin by printing all documents already in the collection,
then will wait for document inserted in the collection and print them.

This is an infinite loop, blocking until one or more documents are inserted.

**important:**

To work with `mongofollow`, each document inserted in the collection needs to
have an `ObjectId` assigned by the MongoDB server as `_id`.

Using a filter
--------------

You can add a filter as second argument. It will then only listen for document
matching that filter.

.. code-block:: python

    for document in mongofollow(collection, {"active": True}):
        print(document)


This will only print documents with a field "active" with a value `True`.
