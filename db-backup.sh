#!/bin/sh

local_file = "data.db"

# Currently deployed on render server
render_user = "srv-cehija6n6mpg3l7jtpcg"
render_host = "ssh.frankfurt.render.com"
render_directory = "/app/instance"
destination_directory = ""

scp "$render_user@$render_host:$render_directory/$local_file" "$destination_directory"
