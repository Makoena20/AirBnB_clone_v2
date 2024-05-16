#!/bin/bash

# Install Nginx if it is not already installed
if ! dpkg -l | grep -q nginx; then
    sudo apt update
    sudo apt install -y nginx
fi

# Create the necessary directories if they don't already exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file to test Nginx configuration
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link, force (-f) to delete it if it already exists
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content
nginx_config="/etc/nginx/sites-available/default"

# Add location block if not already present
if ! grep -q "location /hbnb_static/" $nginx_config; then
    sudo sed -i "/server_name _;/a location /hbnb_static/ {\n\talias /data/web_static/current/;\n}" $nginx_config
fi

# Restart Nginx to apply changes
sudo service nginx restart

# Exit successfully
exit 0

