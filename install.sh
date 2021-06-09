#!/usr/bin/env bash

echo "Installing pyginx ..."
echo "Installing requirements.txt ..."

pip3 install -r requirements.txt

sudo chmod +x pyginx
sudo cp ./pyginx /usr/local/bin

echo "... complete ! run 'sudo pyginx -h' to get started"


