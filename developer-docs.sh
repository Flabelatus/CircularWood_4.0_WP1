#!/bin/bash

DOCS_PATH="./docs/_build/html/index.html"

# Function to build the documentation if it doesn't exist
build_docs() {
    echo "Building documentation..."
    cd ./docs || { echo "Failed to change directory to ./docs"; exit 1; }
    make html
    if [[ $? -ne 0 ]]; then
        echo "Failed to build documentation."
        exit 1
    fi
    cd - > /dev/null || { echo "Failed to return to the original directory"; exit 1; }
}

# Check if the index.html file exists, if not, build the docs
if [[ ! -f "$DOCS_PATH" ]]; then
    echo "Documentation not found at $DOCS_PATH. Attempting to build it..."
    build_docs
fi

# Check again if the index.html file was generated after the build
if [[ ! -f "$DOCS_PATH" ]]; then
    echo "Documentation could not be built. Exiting..."
    exit 1
fi

# Detect the OS
OS_TYPE=$(uname)

# Open the generated index.html in the default browser based on the OS
if [[ "$OS_TYPE" == "Linux" ]]; then
    # Linux
    if command -v xdg-open >/dev/null 2>&1; then
        xdg-open "$DOCS_PATH"
    elif command -v gnome-open >/dev/null 2>&1; then
        gnome-open "$DOCS_PATH"
    elif command -v firefox >/dev/null 2>&1; then
        firefox "$DOCS_PATH"
    else
        echo "No suitable browser found on Linux."
    fi

elif [[ "$OS_TYPE" == "Darwin" ]]; then
    # macOS
    if command -v open >/dev/null 2>&1; then
        open "$DOCS_PATH"
    else
        echo "No suitable browser found on macOS."
    fi

elif [[ "$OS_TYPE" == *"MINGW"* || "$OS_TYPE" == *"CYGWIN"* || "$OS_TYPE" == *"MSYS"* ]]; then
    # Windows via Git Bash, Cygwin, or MSYS
    if command -v start >/dev/null 2>&1; then
        start "$DOCS_PATH"
    else
        echo "No suitable browser found on Windows."
    fi

else
    echo "Unsupported OS: $OS_TYPE"
fi