# Set the syntax version for this Dockerfile
# This enables the use of a newer syntax version if available
# More info: https://docs.docker.com/engine/reference/builder/#syntax
# syntax=docker/dockerfile:1

# Use the Python 3.11 image as the base image
FROM python:3.11

# Sets the maintainer of the project
MAINTAINER FIRST_NAME LAST_NAME "YOUR_EMAIL@gmail.com"

# Set the working directory for the container
# This is the directory where commands will be executed
WORKDIR /src

# Copy the contents of the current directory to the container's working directory
COPY . /src

# Install the project's dependencies
RUN pip install -e .

# Set the default command to run when the container starts
# In this case, run the "main.py" script using the Python interpreter
CMD [ "python", "src/main.py" ]

