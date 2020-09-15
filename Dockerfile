FROM python:latest
# Set the file maintainer (your name - the file's author)
MAINTAINER Pooja Adhikari
# Set env variables used in this Dockerfile (add a unique prefix, such as DOCKYARD)
# Local directory with project source
RUN pip install --upgrade pip 
RUN pip install psycopg2-binary


RUN mkdir /docker_project
WORKDIR /docker_project
RUN mkdir logs

# Copy application source code to SRCDIR
COPY . .
RUN pip install -r requirements.txt

# Install Python dependencies

# Port to expose 
EXPOSE 8000
