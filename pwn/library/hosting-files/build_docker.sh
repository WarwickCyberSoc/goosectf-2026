#!/bin/bash
docker build -t pwn_library .
docker run -p 1337:1337 -it pwn_library