#!/bin/bash
VERSION=$1
if [ -x $VERSION ]; then
    echo "ERROR: You must specify a provider version"
    exit
fi

python3 ./tests/upload_pact.py -b http://127.0.0.1/ -i ./tests/salaryservice-teacherinfoservice.json -v $VERSION
