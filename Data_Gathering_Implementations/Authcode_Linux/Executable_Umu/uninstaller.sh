#!/bin/bash
rm /usr/bin/authcode
sed -i.bak "/ALL ALL = (root) NOPASSWD: \/usr\/bin\/authcode/d" /etc/sudoers
rm -rf $HOME/"Authcode"
rm /etc/profile.d/run_authcode_profile.sh
