#!/bin/bash

curl -u admin:admin123 -X 'POST' \
  'http://localhost:8082/service/rest/v1/repositories/maven/hosted' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'NX-ANTI-CSRF-TOKEN: 0.0803152062108512' \
  -d '{
  "name": "staging-test",
  "online": true,
  "storage": {
    "blobStoreName": "maven",
    "strictContentTypeValidation": true,
    "writePolicy": "ALLOW_ONCE"
  },
  "cleanup": null,
  "maven": {
    "versionPolicy": "RELEASE",
    "layoutPolicy": "STRICT",
    "contentDisposition": "INLINE"
  },
  "component": {
    "proprietaryComponents": false
  },
  "format": "maven2",
  "type": "hosted"
}'



