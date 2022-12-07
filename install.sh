#! /bin/sh

ln -sf $PWD/aliyun-share /bin
sed "s#_USER_#${SUDO_USER:-$USER}#; s#_PWD_#$PWD#" alibrary.service > /etc/systemd/system/alibrary.service
systemctl daemon-reload
systemctl enable alibrary
systemctl start alibrary
