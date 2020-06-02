#!/bin/bash

VERSION=$(grep 'version \=' pyproject.toml | cut -d'=' -f2 | tr -d '"'| tr -d ' ')

docker build . --tag osol:$VERSION
