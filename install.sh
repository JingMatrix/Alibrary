#! /bin/sh

mkdir -p $HOME/.local/bin
ln -sf $PWD/aliyun-share $HOME/.local/bin
mkdir -p $HOME/.config/systemd/user
sed "s#_PWD_#$PWD#" alibrary.service > $HOME/.config/systemd/user/alibrary.service
systemctl --user daemon-reload
systemctl --user enable alibrary
systemctl --user start alibrary
