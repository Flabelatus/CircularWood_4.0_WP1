#!/bin/sh

echo "Connecting to the dev server ..."
echo "This may take several seconds"

local_file="data.db"

# Currently deployed on render server
render_user="srv-cno1u0tjm4es73ceindg"
render_host="ssh.frankfurt.render.com"

# The directory of the data.db
render_directory_db="/app/instance"

# The directory of the static
render_directory_static="/app/static"

# Get the root directory
root_directory=$(pwd)

# Get the data.db directory
destination_sub_dir_db="instance"
destination_directory_db="$root_directory/$destination_sub_dir_db"

# Get the image directory
destination_sub_dir_static="static"
destination_directory_static="$root_directory/$destination_sub_dir_static"

# Ensure local directories exist
if [ ! -d "$destination_directory_db" ]; then
    mkdir -p "$destination_directory_db"
    if [ $? -ne 0 ]; then
        echo "Failed to create directory: $destination_directory_db"
        exit 1
    fi
fi

if [ ! -d "$destination_directory_static" ]; then
    mkdir -p "$destination_directory_static"
    if [ $? -ne 0 ]; then
        echo "Failed to create directory: $destination_directory_static"
        exit 1
    fi
fi

# Copy the data.db
scp "$render_user@$render_host:$render_directory_db/$local_file" "$destination_directory_db"
if [ $? -ne 0 ]; then
    echo "Backup of data.db failed."
else
    echo "Backup of data.db successful!"
fi

# Copy the contents of the static directory
ssh "$render_user@$render_host" "tar czf - -C $render_directory_static ." | tar xzf - -C "$destination_directory_static"
if [ $? -ne 0 ]; then
    echo "Backup of static directory failed."
else
    echo "Backup of static directory successful!"
fi

# Keep the terminal window open
read -p "Press Enter to close this window..."
