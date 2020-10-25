FROM python:3.8.6-slim-buster

# The enviroment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

# Instal gcc compiler to build dependencies and link the python and python3 commands
RUN apt-get update && apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*
RUN ln -sv /usr/bin/python3 /usr/bin/python

# Upgrade pip
RUN pip install --upgrade pip

# Install packages
RUN pip install streamlit
RUN pip install pandas
RUN pip install fastapi
RUN pip install hypercorn
RUN pip install sweetviz
RUN pip install dataprep

# Copy data app into container
ADD . /app

# Work in the application directory
WORKDIR /app