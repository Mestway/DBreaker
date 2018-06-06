#!/bin/sh

echo "[CONFIG] Initializing MySQL..."

# init mysql service
find /var/lib/mysql/mysql -exec touch -c -a {} + && service mysql start

# replace "-" with "_" for database username
MAINDB="test_db"
USER="dbtest"
PASSWORD="dbtest"

# the rootpassword was defined in Dockerfile
root_password="root"

echo "[CONFIG] Creating database and user..."

mysql -uroot --password=$root_password -e "CREATE DATABASE IF NOT EXISTS ${MAINDB} /*\!40100 DEFAULT CHARACTER SET utf8 */;"
mysql -uroot --password=$root_password -e "CREATE USER IF NOT EXISTS ${USER}@localhost IDENTIFIED BY '${PASSWORD}';"
mysql -uroot --password=$root_password -e "GRANT ALL PRIVILEGES ON ${MAINDB}.* TO '${USER}'@'localhost';"
mysql -uroot --password=$root_password -e "FLUSH PRIVILEGES;"

echo "[CONFIG] Building Calcite-MySQL interface..."

# build the connector
cd calcite_interface
mvn clean compile assembly:single
cd ..
