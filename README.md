# TwitterAPI-with-OpenSearch Lambda function to send index to OpenSearch and to be triggered by S3 put object
>From Streaming Data to COVID-19 Twitter Analysis: Using AWS Lambda, Kinesis Firehose and Elasticsearch
>Docker used for MacOS, since python pip will download dependencies in C++ but we need it unix compatable files, so we use Docker invironment.
>CMD:  docker build -t hello-world . && docker run --rm  hello-world 

in DockerFile change the following \n

ENV AWS_DEFAULT_REGION [YOUR REGION] \n
ENV AWS_ACCESS_KEY_ID [YOUR ACCESS_KEY_ID] \n
ENV AWS_SECRET_ACCESS_KEY [YOUR SECRET_ACCESS_KEY]
