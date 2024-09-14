#!/bin/bash

ENDPOINT="/api-docs"
SETTINGS_FILE="./settings.yml"

# yaml parser tool
YQ="yq"

# Function to install yq based on the operating system
install_yq() {
  if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Install yq on Linux
    echo "Installing yq for Linux..."
    sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/download/v4.16.1/yq_linux_amd64
    sudo chmod +x /usr/local/bin/yq
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    # Install yq on macOS using Homebrew
    echo "Installing yq for macOS..."
    brew install yq
  elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "mingw"* ]]; then
    # Install yq on Windows (MSYS/MinGW environment)
    echo "Installing yq for Windows..."
    YQ_VERSION="v4.16.1"
    YQ_BINARY="yq_windows_amd64.exe"
    curl -L -o yq.exe https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/${YQ_BINARY}
    chmod +x yq.exe
    mv yq.exe ./tools/yq.exe
    YQ="./tools/yq.exe"
  else
    echo "Unsupported OS. Please install yq manually: https://github.com/mikefarah/yq"
    exit 1
  fi
}

# Check if yq is installed, install it if not found
if ! command -v yq &> /dev/null; then
  echo "yq not found. Installing yq..."
  install_yq
else
  echo "yq is already installed."
fi

URL=""
ENVIRONMENT=$($YQ e '.api.server.environment.selected_mode' $SETTINGS_FILE)

if [[ "$ENVIRONMENT" == "development" ]]; then
    URL="$($YQ e '.api.server.environment.modes.development.url' $SETTINGS_FILE)${ENDPOINT}"
else
    URL="$($YQ e '.api.server.environment.modes.production.url' $SETTINGS_FILE)${ENDPOINT}"
fi

# Detect the OS
OS_TYPE=$(uname)

if [[ "$OS_TYPE" == "Linux" ]]; then
    # Linux
    if command -v xdg-open >/dev/null 2>&1; then
        xdg-open "$URL"
    elif command -v gnome-open >/dev/null 2>&1; then
        gnome-open "$URL"
    elif command -v firefox >/dev/null 2>&1; then
        firefox "$URL"
    else
        echo "No suitable browser found on Linux."
    fi

elif [[ "$OS_TYPE" == "Darwin" ]]; then
    # macOS
    if command -v open >/dev/null 2>&1; then
        open "$URL"
    else
        echo "No suitable browser found on macOS."
    fi

elif [[ "$OS_TYPE" == *"MINGW"* || "$OS_TYPE" == *"CYGWIN"* || "$OS_TYPE" == *"MSYS"* ]]; then
    # Windows via Git Bash, Cygwin, or MSYS
    if command -v start >/dev/null 2>&1; then
        start "$URL"
    else
        echo "No suitable browser found on Windows."
    fi

else
    echo "Unsupported OS: $OS_TYPE"
fi