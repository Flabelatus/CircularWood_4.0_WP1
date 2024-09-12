#!/bin/bash

SETTINGS_FILE="./settings.yml"
DATABASE_HOST="localhost"
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

# Extracting other settings
DATABASE_USER=$($YQ e '.api.database.user // "null"' $SETTINGS_FILE)
DATABASE_URL=$($YQ e '.api.database.uri // "sqlite:///instance/data.db"' $SETTINGS_FILE)

DATABASE_PASSWORD=$($YQ e '.api.database.password // "null"' $SETTINGS_FILE)
DATABASE_DB=$($YQ e '.api.database.dbname // "null"' $SETTINGS_FILE)

# Extract allowedOrigins and join them into a single line separated by commas
ALLOWED_ORIGINS=$($YQ e '.api.configs.cors.allowed_origins[]' $SETTINGS_FILE | paste -sd "," -)

# Extract JWT settings
JWT_SECRET=$($YQ e '.api.security.jwt.secret' $SETTINGS_FILE)
JWT_EXPIRATION_TIME=$($YQ e '.api.security.jwt.expirationTime' $SETTINGS_FILE)
JWT_ISSUER=$($YQ e '.api.security.jwt.issuer' $SETTINGS_FILE)
JWT_AUDIENCE=$($YQ e '.api.security.jwt.audience' $SETTINGS_FILE)

# Extract other environment variables from the settings
URL=$($YQ e '.api.server.environment.url // "http://localhost:5050"' $SETTINGS_FILE)
API_LOG_LEVEL=$($YQ e '.api.server.environment.logging // "DEBUG"' $SETTINGS_FILE)

# Generate the .env file
cat > .env <<EOL
URL=$URL
API_LOG_LEVEL=$API_LOG_LEVEL
DATABASE_URL=$DATABASE_URL
DATABASE_HOST=$DATABASE_HOST
DATABASE_USER=$DATABASE_USER
DATABASE_PASSWORD=$DATABASE_PASSWORD
DATABASE_DB=$DATABASE_DB
CONFIG_FILE=./settings.yml
ALLOWED_ORIGINS=$ALLOWED_ORIGINS
JWT_SECRET=$JWT_SECRET
JWT_EXPIRATION_TIME=$JWT_EXPIRATION_TIME
JWT_ISSUER=$JWT_ISSUER
JWT_AUDIENCE=$JWT_AUDIENCE
EOL

echo ".env file has been generated from settings.yml"
