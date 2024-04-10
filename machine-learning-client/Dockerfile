# in Docker, it is common to base a new image on a previously-created image
FROM python:3.8-slim-buster
RUN apt-get update && \
    apt-get -y install libgl1-mesa-glx 
RUN apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6
# Set the working directory in the image
WORKDIR /app
# install dependencies into the image - doing this first will speed up subsequent builds, as Docker will cache this step
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
# the ADD command is how you add files from your local machine into a Docker image
# Copy the current directory contents into the container at /app
ADD . .
# Run app.py when the container launches
CMD [ "python3", "main.py"]