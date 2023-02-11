#!/bin/bash

pipenv install
cd `pipenv --venv`/lib/python3.8/site-packages/
zip -r /var/task/my-deployment-package.zip .
cd -
zip -r -g my-deployment-package.zip .
aws lambda update-function-code --function-name s3-twitter-to-es-python --zip-file fileb://my-deployment-package.zip
myhandle.handler