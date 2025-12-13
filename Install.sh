#!/bin/bash

echo "Instalando daemon servermonitor..."

sudo cp daemon/smarthelper.py /usr/local/bin/
sudo chmod +x /usr/local/bin/smarthelper.py

sudo cp daemon/servermonitor.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable --now servermonitor.service

echo "Instalado. Rodando como root."