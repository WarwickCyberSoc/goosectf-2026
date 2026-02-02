#!/bin/bash
docker build -t pwn_broken_system .
docker run -p 1337:1337 -it pwn_broken_system