#!/bin/bash

# Set the Skaffold version to download
SKAFFOLD_VERSION="1.31.0"

# Set the operating system and architecture
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m | sed 's/x86_64/amd64/')

# Download and extract the Skaffold binary
curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64 && \
sudo install skaffold /usr/local/bin/

