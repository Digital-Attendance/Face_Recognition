# Use the AWS Lambda Python 3.12 base image
FROM public.ecr.aws/lambda/python:3.12

RUN microdnf update -y && \
    microdnf install -y cmake gcc-c++ make git


# Upgrade pip and install required packages
RUN pip install --upgrade pip  setuptools && \
    pip install aiofiles  boto3 && \
    pip install face_recognition

# Copy your Lambda function code into the container
# Assume your file is named "face_recognition_lambda.py"
COPY . ${LAMBDA_TASK_ROOT}

# Set the CMD to your Lambda handler function
CMD [ "app.lambda_handler" ]
