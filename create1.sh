#!/bin/bash

curl -u admin:admin123 -X 'POST' \
  'http://localhost:8082/service/rest/v1/repositories/maven/hosted' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'NX-ANTI-CSRF-TOKEN: 0.0803152062108512' \
  -d '{
  "name": "internal2",
  "online": true,
  "storage": {
    "blobStoreName": "default",
    "strictContentTypeValidation": true,
    "writePolicy": "allow_once"
  },
  "cleanup": {
    "policyNames": [
      "string"
    ]
  },
  "component": {
    "proprietaryComponents": true
  },
  "maven": {
    "versionPolicy": "MIXED",
    "layoutPolicy": "STRICT",
    "contentDisposition": "ATTACHMENT"
  }
}'



