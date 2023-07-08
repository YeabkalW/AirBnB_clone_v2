#!/usr/bin/env bash
# sets up web servers for web_static deployment

#--Updating the packages
sudo apt-get -y update
sudo apt-get -y install nginx

#--configures firewall
sudo ufw allow 'Nginx HTTP'
echo -e "\e[1;35m Enables In-Bound NGINX HTTP \e[0m"
echo

#--Creates needed directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
echo -e "\e[1;35m created directories \e[0m"
echo

# Creates indes.html file
sudo touch /data/web_static/releases/test/index.html
echo -e "e\[1;35m index.html file created \e[0m"
echo

#--Inserts test string
echo "<h1>Welcome to www.beta-scribbles.tech</h1>" > /data/web_static/releases/test/index.html
echo -e "\e[1;35m Test string Inserted\e[0m"
echo

#--Handles Overwriting
if [ -d "/data/web_static/current" ];
then
    echo "path /data/web_static/current exists"
    sudo rm -rf /data/web_static/current;
fi;
echo -e "\e[1;35m Handling Overwriting Isues \e[0m"
echo

#--Creates symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
echo -e "e\[1;30m /Creating Symbollic \e[0m"

#-- Changes Ownership of a /data
sudo chown -hR ubuntu:ubuntu /data
echo -e "e\[1;35m /Directory ownership transfer to ubuntu \e[0m"

sudo sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

sudo ln -sf '/etc/nginx/sites-available/default' '/etc/nginx/sites-enabled/default'
echo -e "\e[1;35m Symbolic link created\e[0m"
echo

#--restart NGINX
sudo service nginx restart
echo -e "\e[1;35m restarted NGINX\e[0m"
