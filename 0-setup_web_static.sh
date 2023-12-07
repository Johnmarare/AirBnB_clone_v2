#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static


# Install Nginx if not installed
if ! command -v nginx &> /dev/null; then
	sudo apt-get update
	sudo apt-get -y install nginx
fi

# Create necessary folders
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file with simple content
echo "<html>
  <head>
  </head>
  <body>
    Test Nginx Configuration!
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create or recreate symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give owenership of the data folder to user and group
sudo chown -hR ubuntu:ubuntu /data/

# Update Nginx Configuration to serve the content
server_config="
server {
	listen 80 default_server;
	listen [::]:80 default_server;
	add_header X-Served-By $HOSTNAME;
	root /var/www/html;

	location /hbnb_static {
		alias /data/web_static/current/;
	}
	
	error_page 404 /404.html;
	location /404 {
		root /var/www/html;
		internal;
	}
}
"

echo "$server_config" | sudo tee /etc/nginx/sites-available/default > /dev/null
# Restart Nginx
sudo service nginx restart
