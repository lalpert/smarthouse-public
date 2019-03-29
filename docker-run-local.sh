#!/bin/bash
docker build -t app . && docker run -p 80:80 --env-file=.env --env RUN_DB=false --env DEBUG=true app
