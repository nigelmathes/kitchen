# ============== Base Container ==============
FROM python:3.9.5-slim AS base-kitchen

# Instal build dependencies
RUN apt-get update && apt-get install -y gcc g++ && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# API serving packages
RUN pip install --no-cache-dir fastapi hypercorn aiofiles jinja2

# Data exploration tools
RUN pip install --no-cache-dir dataprep streamlit

# Data IO packages
RUN pip install --no-cache-dir anyconfig s3fs fsspec pyarrow

# Data science utilities
RUN pip install --no-cache-dir pandas scikit-learn joblib opencv-python-headless

# Work in the application directory
WORKDIR /app

# Copy app code
COPY . /app

# ============== Dev environment ==============
FROM base-kitchen AS dev-kitchen

# Instal runtime dependencies
RUN apt-get update && apt-get install -y curl git && \
    rm -rf /var/lib/apt/lists/*

# Jupyter Lab and dev tools
RUN pip install --no-cache-dir jupyterlab black pylint

# Install VS Code-Server and useful Python Extensions
RUN curl -fsSL https://code-server.dev/install.sh | sh
RUN code-server --install-extension ms-python.python --force
RUN code-server --install-extension njpwerner.autodocstring	--force
RUN code-server --install-extension LittleFoxTeam.vscode-python-test-adapter --force
RUN code-server --install-extension dongli.python-preview --force
RUN code-server --install-extension CoenraadS.bracket-pair-colorizer-2 --force
RUN code-server --install-extension jdinhlife.gruvbox --force
