#!/usr/bin/env bash

if [[ "$OSTYPE" == "linux-gnu"* ]]; then

  echo "Installing pyginx ..."

  echo "Installing pip3 ..."
  sudo apt update
  sudo apt install python3-pip -y

  echo "Installing requirements.txt ..."

  curl https://raw.githubusercontent.com/ValentinKolb/pyginx/main/requirements.txt | pip3 install -r

  curl https://raw.githubusercontent.com/ValentinKolb/pyginx/main/pyginx > /usr/local/bin/pyginx
  sudo chmod +x /usr/local/bin/pyginx

  echo "... complete ! run 'sudo pyginx -h' to get started"
  exit 0

else

  echo "Your OS is not supported!"
  exit 1

fi


