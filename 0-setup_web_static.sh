#!/usr/bin/env bash
# This script sets up your web servers for the deployment of web_static

# Update package list and install Nginx if it is not already installed
if ! dpkg -l | grep -q nginx; then
    apt-get update
    apt-get install -y nginx
fi

# Create the required directories if they don't already exist
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file for testing Nginx configuration
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create a symbolic link to the test release
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Check if the user 'ubuntu' exists, if not, use a fallback user
if id "ubuntu" &>/dev/null; then
    USER="ubuntu"
else
    USER=$(whoami)
fi

# Give ownership of the /data/ folder to the detected user and group recursively
chown -R "$USER":"$USER" /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
nginx_conf="/etc/nginx/sites-available/default"
if ! grep -q "location /hbnb_static" "$nginx_conf"; then
    sed -i '/server_name _;/a \\
    location /hbnb_static/ {\\
        alias /data/web_static/current/;\\
    }' "$nginx_conf"
fi

# Restart Nginx to apply changes
service nginx restart

# Exit successfully
exit 0

