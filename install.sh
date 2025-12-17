#!/bin/bash
if [ "$EUID" -ne 0 ]; then
  echo "Por favor, execute como root."
  exit 1
fi

set -e

echo "Instalando dependências do sistema..."
sudo apt update
sudo apt install -y \
    python3 \
    python3-pip \
    smartmontools \
    nvme-cli \
    lm-sensors \
    util-linux \
    iputils-ping \
    pciutils \
    iproute2


INSTALL_DIR="/opt/servermonitor"

echo ">>> Copiando arquivos para $INSTALL_DIR"
sudo rm -rf "$INSTALL_DIR"
sudo mkdir -p "$INSTALL_DIR"
sudo cp -r ./* "$INSTALL_DIR"
sudo chown -R root:root "$INSTALL_DIR"

cd $INSTALL_DIR

echo "Criando venv..."
python3 -m venv venv

echo "Instalando dependências Python..."
source venv/bin/activate
sudo "$INSTALL_DIR/venv/bin/pip" install --upgrade pip
sudo "$INSTALL_DIR/venv/bin/pip" install -r requirements.txt
deactivate

echo ">>> Criando serviço Flask"
sudo tee /etc/systemd/system/servermonitor.service > /dev/null <<EOF
[Unit]
Description=Server Monitor Web
After=network.target

[Service]
Type=simple
User=leonardo
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo ">>> Criando serviço SMART daemon"
sudo tee /etc/systemd/system/servermonitor-smart.service > /dev/null <<EOF
[Unit]
Description=Server Monitor SMART Daemon

[Service]
Type=simple
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/smarthelper.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo ">>> Ativando serviços"
sudo systemctl daemon-reload
sudo systemctl enable servermonitor
sudo systemctl enable servermonitor-smart
sudo systemctl restart servermonitor
sudo systemctl restart servermonitor-smart

echo ">>> Instalação finalizada. Acessa em http://localhost:5000"