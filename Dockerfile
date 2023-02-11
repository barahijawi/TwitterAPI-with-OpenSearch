FROM lambci/lambda:build-python3.8

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY . ${LAMBDA_TASK_ROOT}

ENV AWS_DEFAULT_REGION [YOUR REGION]
ENV AWS_ACCESS_KEY_ID [YOUR ACCESS_KEY_ID]
ENV AWS_SECRET_ACCESS_KEY [YOUR SECRET_ACCESS_KEY]

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
#CMD [ "myhandle.handler"]
RUN ["chmod", "+x", "dockerCmd.sh"]
CMD ./dockerCmd.sh