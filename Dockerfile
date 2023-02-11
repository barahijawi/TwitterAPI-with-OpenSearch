#FROM public.ecr.aws/lambda/python:3.8
FROM lambci/lambda:build-python3.8

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY . ${LAMBDA_TASK_ROOT}

ENV AWS_DEFAULT_REGION us-east-1
ENV AWS_ACCESS_KEY_ID AKIA2ARFM6S5YKTODX7F
ENV AWS_SECRET_ACCESS_KEY fP/VotJgSgOfnhd5SXEs27j+4Cj8O511Px5BIAzF

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
#CMD [ "myhandle.handler"]
RUN ["chmod", "+x", "dockerCmd.sh"]
CMD ./dockerCmd.sh


################################
#FROM lambci/lambda:build-python3.8

# Install the function's dependencies using file requirements.txt
# from your project folder.

#COPY requirements.txt  .
#RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
#
## Copy function code
#COPY . ${LAMBDA_TASK_ROOT}
#ENV AWS_DEFAULT_REGION us-east-1
#ENV AWS_ACCESS_KEY_ID AKIA2ARFM6S5YKTODX7F
#ENV AWS_SECRET_ACCESS_KEY fP/VotJgSgOfnhd5SXEs27j+4Cj8O511Px5BIAzF
#
##COPY . .
##RUN ["chmod", "+x", "dockerCmd.sh"]
#
##CMD ./dockerCmd.sh
#
## Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
#CMD [ "myhandle.handler" ]
##CMD ./dockerCmd.sh