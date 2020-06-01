#!/bin/bash

docker run -d \
       --publish 8501:8501 \
       osol:${1}
