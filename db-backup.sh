#!/bin/sh

echo "Connecting to the server ..."
echo ""
echo "This may take several seconds"

local_file="data.db"

# Currently deployed on render server
render_user="srv-cehija6n6mpg3l7jtpcg"
render_host="ssh.frankfurt.render.com"
render_directory="/app/instance"

# Get the root directory
root_directory=$(pwd)
destination_sub_dir="instance"
destination_directory="$root_directory/$destination_sub_dir"

scp "$render_user@$render_host:$render_directory/$local_file" "$destination_directory"

# Check if SCP was successful
if [ $? -eq 0 ]; then
    echo "Backup successful!"
else
    echo "Backup failed."
fi

# Keep the terminal window open
read -p "Press Enter to close this window..."
