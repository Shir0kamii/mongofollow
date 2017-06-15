#!/bin/bash
set -ev

if [ ! -z "$TRAVIS_TAG" ]; then
	flit publish
fi
