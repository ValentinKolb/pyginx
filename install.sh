#!/usr/bin/env bash

# This script first installs all dependencies of pyginx and then pyginx
# Author:  Valentin Kolb
# Version: 1.5
# License: MIT

set -e
set -o pipefail

# move to home dir
cd

# initial cleanup
if [ -e "/etc/pyginx.d" ];then sudo rm -rf "/etc/pyginx.d" ; fi
if [ -e "/usr/local/bin/pyginx" ];then sudo rm "/usr/local/bin/pyginx" ; fi

echo "Installing pyginx ..."

echo "Installing pip3 ..."
sudo apt update
sudo apt install python3-pip -y

echo "Installing requirements.txt ..."
curl https://raw.githubusercontent.com/ValentinKolb/pyginx/main/requirements.txt > pyginx_requirements.txt
sudo pip3 install -r pyginx_requirements.txt
rm pyginx_requirements.txt

echo "Downloading config files ..."
sudo mkdir /etc/pyginx.d
sudo curl -o /etc/pyginx.d/http.templ https://raw.githubusercontent.com/ValentinKolb/pyginx/main/pyginx.d/http.templ
sudo curl -o /etc/pyginx.d/stream.templ https://raw.githubusercontent.com/ValentinKolb/pyginx/main/pyginx.d/stream.templ
sudo curl -o /etc/pyginx.d/pyginx.ini https://raw.githubusercontent.com/ValentinKolb/pyginx/main/pyginx.d/pyginx.ini

echo "Installing pyginx ..."
sudo curl -o /usr/local/bin/pyginx https://raw.githubusercontent.com/ValentinKolb/pyginx/main/pyginx
sudo chmod +x /usr/local/bin/pyginx
echo "... install complete"
echo "Version:"
sudo pyginx --version
echo "Run 'sudo pyginx -h' to get started."

exit 0
