#!/usr/bin/env bash

# This script first installs all dependencies of pyginx and then pyginx
# Author:  Valentin Kolb
# Version: 1.5
# License: MIT

set -e
set -o pipefail

echo "Installing pyginx ..."

echo "Installing pip3 ..."
sudo apt update
sudo apt install python3-pip -y

echo "Installing requirements.txt ..."
curl https://raw.githubusercontent.com/ValentinKolb/pyginx/main/requirements.txt > pyginx_requirements.txt
pip3 install -r pyginx_requirements.txt
rm pyginx_requirements.txt

echo "Installing pyginx ..."
curl https://raw.githubusercontent.com/ValentinKolb/pyginx/main/pyginx > pyginx
sudo mv pyginx /usr/local/bin/
sudo chmod +x /usr/local/bin/pyginx

echo "... complete ! run 'sudo pyginx -h' to get started"
exit 0
