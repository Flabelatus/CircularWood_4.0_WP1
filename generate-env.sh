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
DATABASE_USER=$($YQ e '.data_service_api.database.user // "null"' $SETTINGS_FILE)
DATABASE_URL=$($YQ e '.data_service_api.database.uri // "sqlite:///instance/data.db"' $SETTINGS_FILE)

DATABASE_PASSWORD=$($YQ e '.data_service_api.database.password // "null"' $SETTINGS_FILE)
DATABASE_DB=$($YQ e '.data_service_api.database.dbname // "null"' $SETTINGS_FILE)

# Extract allowedOrigins and join them into a single line separated by commas
ALLOWED_ORIGINS=$($YQ e '.data_service_api.configs.cors.allowed_origins[]' $SETTINGS_FILE | paste -sd "," -)

# Extract JWT settings
# JWT_SECRET=$($YQ e '.api.security.jwt.secret' $SETTINGS_FILE)
# JWT_EXPIRATION_TIME=$($YQ e '.api.security.jwt.expirationTime' $SETTINGS_FILE)
JWT_ISSUER=$($YQ e '.data_service_api.security.jwt.issuer' $SETTINGS_FILE)
JWT_AUDIENCE=$($YQ e '.data_service_api.security.jwt.audience' $SETTINGS_FILE)


URL=""
ENVIRONMENT=$($YQ e '.api.server.environment.selected_mode' $SETTINGS_FILE)

if [[ "$ENVIRONMENT" == "development" ]]; then
    URL="$($YQ e '.data_service_api.server.environment.modes.development.url' $SETTINGS_FILE)${ENDPOINT}"
else
    URL="$($YQ e '.data_service_api.server.environment.modes.production.url' $SETTINGS_FILE)${ENDPOINT}"
fi

API_LOG_LEVEL_DEBUG=$($YQ e '.data_service_api.server.environment.modes.development.logging' $SETTINGS_FILE)
API_LOG_LEVEL_INFO=$($YQ e '.data_service_api.server.environment.modes.production.logging' $SETTINGS_FILE)

# Generate the .env file
cat > .env <<EOL
URL=$URL
ENVIRONMENT=$ENVIRONMENT
API_LOG_LEVEL_INFO=$API_LOG_LEVEL_INFO
API_LOG_LEVEL_DEBUG=$API_LOG_LEVEL_DEBUG
DATABASE_URL=$DATABASE_URL
DATABASE_HOST=$DATABASE_HOST
DATABASE_USER=$DATABASE_USER
DATABASE_PASSWORD=$DATABASE_PASSWORD
DATABASE_DB=$DATABASE_DB
CONFIG_FILE=./settings.yml
ALLOWED_ORIGINS=$ALLOWED_ORIGINS
JWT_ISSUER=$JWT_ISSUER
JWT_AUDIENCE=$JWT_AUDIENCE
EOL

echo ".env file has been generated from settings.yml"
