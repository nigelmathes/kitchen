# 1st stage: Base Kitchen dependencies
FROM python:3.9.5-slim-buster AS base-kitchen

# The enviroment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

# Instal gcc compiler to build dependencies and link the python and python3 commands
RUN apt-get update && apt-get install -y gcc curl git && \
    rm -rf /var/lib/apt/lists/*
RUN ln -sv /usr/bin/python3 /usr/bin/python

# Upgrade pip
RUN pip install --upgrade pip

# Install packages
# Data IO packages

# API serving packages
RUN pip install fastapi
RUN pip install hypercorn
RUN pip install aiofiles
RUN pip install jinja2

# Data exploration tools
RUN pip install dataprep
RUN pip install streamlit

# Config parsing
RUN pip install anyconfig

# Interact with all data as a file system
RUN pip install s3fs
RUN pip install fsspec

# Data science utilities
RUN pip install pandas
RUN pip install scikit-learn
RUN pip install joblib
RUN pip install opencv-python-headless

# Copy data app into container
COPY . /app

# Work in the application directory
WORKDIR /app

# 2nd stage: Dev dependencies
FROM base-kitchen AS dev-kitchen

# Jupyter Lab
RUN pip install jupyterlab

# Install VS Code-Server and useful Python Extensions
RUN curl -fsSL https://code-server.dev/install.sh | sh
RUN code-server --install-extension ms-python.python --force
RUN code-server --install-extension njpwerner.autodocstring	--force
RUN code-server --install-extension LittleFoxTeam.vscode-python-test-adapter --force
RUN code-server --install-extension dongli.python-preview --force
RUN code-server --install-extension CoenraadS.bracket-pair-colorizer-2 --force
RUN code-server --install-extension jdinhlife.gruvbox --force

# Python formatting and linting support
RUN pip install black
RUN pip install pylint
