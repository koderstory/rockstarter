#!/bin/bash

GREEN='\033[1;36m'
WHITE='\033[1;37m'

echo -ne "Domain Name:\n"
read DOMAIN

printf "\n\nChoose Action:\n1) Setup Server\n2) Delete Website (You can't undo)\n"
read ACTION


if [ -z "$ACTION" ] 
then
    printf "===================================\n"
	printf "NO ACTION SELECTED 🤷‍♂️\n"
    printf "===================================\n"



elif [ $ACTION -eq 1 ]
then

echo "[Unit]
Description=gunicorn socket -> $DOMAIN

[Socket]
ListenStream=/run/gunicorn_$DOMAIN.sock

[Install]
WantedBy=sockets.target
"| sudo tee /etc/systemd/system/gunicorn_$DOMAIN.socket >> $PWD/logs/deploy.log


echo "> Socket file is created" >> $PWD/logs/deploy.log


sudo chmod -R 755 $PWD/logs


echo "[Unit]
Description=gunicorn $DOMAIN daemon
Requires=gunicorn_$DOMAIN.socket
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$PWD
ExecStart=$PWD/.venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn_$DOMAIN.sock \
	  --chdir $PWD \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
" | sudo tee /etc/systemd/system/gunicorn_$DOMAIN.service >> $PWD/logs/deploy.log


echo "> Service file is created" >> $PWD/logs/deploy.log


sudo systemctl start gunicorn_$DOMAIN.socket
sudo systemctl enable gunicorn_$DOMAIN.socket
curl --unix-socket /run/gunicorn_$DOMAIN.sock localhost >> $PWD/logs/deploy.log
sudo systemctl daemon-reload


printf "\n${GREEN}✅ systemd is done ${WHITE}\n"


echo "server {
    listen 80;
    server_name $DOMAIN;
    error_log $PWD/logs/nginx.error.log;
    access_log $PWD/logs/nginx.access.log;
    rewrite_log on;
    server_tokens off;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection '1; mode=block';

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn_$DOMAIN.sock;
    }
}
" | sudo tee /etc/nginx/sites-available/$DOMAIN >> $PWD/logs/deploy.log
sudo ln -s /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled
sudo systemctl restart nginx


elif [ $ACTION -eq 2 ]
then 


sudo systemctl stop gunicorn_$DOMAIN.service
sudo systemctl disable gunicorn_$DOMAIN.service

sudo systemctl stop gunicorn_$DOMAIN.socket
sudo systemctl disable gunicorn_$DOMAIN.socket

sudo rm /etc/systemd/system/gunicorn_$DOMAIN.service
sudo rm /etc/systemd/system/gunicorn_$DOMAIN.socket

sudo systemctl daemon-reload
sudo systemctl reset-failed

sudo rm /etc/nginx/sites-available/$DOMAIN
sudo rm /etc/nginx/sites-enabled/$DOMAIN

sudo systemctl restart nginx

printf "😭 YOU DELETED WEBSITE 😭\n"


fi
