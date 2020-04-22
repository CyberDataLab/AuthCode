#!/bin/bash
apt-get install -y wmctrl
apt-get install -y gnome-terminal
apt-get install -y xdotool
apt-get install -y libnotify-bin
apt-get install -y python3.7
cp authcode /usr/bin/authcode
sed -i.bak "/ALL ALL = (root) NOPASSWD: \/usr\/bin\/authcode/d" /etc/sudoers
echo -e "ALL ALL = (root) NOPASSWD: /usr/bin/authcode\n" | tee -a /etc/sudoers
cp run_authcode_profile.sh /etc/profile.d/run_authcode_profile.sh
authcode
