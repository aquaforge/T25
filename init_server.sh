#!/bin/bash
if [ "$#" -ne 1 ]
then
echo "Incorrect number of arguments"
exit 1
fi

#swap
cd /
fallocate -l 3G /swapfile
# ls -lh /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
# swapon --show
# free -h
# top


apt update 
apt upgrade -y
apt install -y python3-pip python3-venv mysql-server net-tools git ufw
# scp "C:\Users\User\Downloads\init_server.sh" root@XX.XX.XX.XX:/app


#firewall
ufw allow ssh
ufw allow mysql
ufw enable
#ufw status verbose


#mysql
mysqld --initialize
mysql -u root -e "CREATE SCHEMA t25;"
#mysql -u root -e "show schemas;"

mysql -u root -e "CREATE USER 't25_user'@'%' IDENTIFIED BY '$1';"
mysql -u root -e "GRANT ALL ON t25.* TO 't25_user'@'%';"
#mysql -u root -e "SELECT user,plugin,host FROM mysql.user;"

sed -i 's/bind-address\t\t= 127.0.0.1/bind-address\t\t= 0.0.0.0/g' /etc/mysql/mysql.conf.d/mysqld.cnf
systemctl restart mysql


#path

#source
cd /
mkdir -p /app/t25
chmod -R 777 /app

cd /app/t25
#git pull
cd /


#python
python3 -m venv /app/t25/venv
source /app/t25/venv/bin/activate
pip install -r requirements.txt
deactivate
