#!/bin/bash
if [ "$EUID" -ne 0 ]; then
  echo "Por favor, execute como root."
  exit 1
fi

INSTALL_DIR="/opt/servermonitor"

rm -rf "$INSTALL_DIR"
sudo systemctl disable servermonitor.service
sudo systemctl disable servermonitor-smart.service
sudo systemctl stop servermonitor.service
sudo systemctl stop servermonitor-smart.service
sudo rm /etc/systemd/system/servermonitor.service
sudo rm /etc/systemd/system/servermonitor-smart.service
sudo rm /var/run/servermonitor.sock 
sudo systemctl daemon-reload
echo "Server Monitor desinstalado com sucesso."