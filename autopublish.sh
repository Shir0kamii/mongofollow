#!/bin/bash
set -ev

if [ ! -z "$TRAVIS_TAG" ]; then
	flit publish
	echo "Published version $TRAVIS_TAG to PyPi"
fi
echo "nothing to publish"
