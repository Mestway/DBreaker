# replace "-" with "_" for database username
MAINDB="test_database"
USER_NAME="dbtest"
PASSWORD="dbtest"

#mysql -e "CREATE DATABASE ${MAINDB} /*\!40100 DEFAULT CHARACTER SET utf8 */;"
#mysql -e "CREATE USER ${USER_NAME}@localhost IDENTIFIED BY '${PASSWORD}';"
#mysql -e "GRANT ALL PRIVILEGES ON ${MAINDB}.* TO '${USER_NAME}'@'localhost';"
#mysql -e "FLUSH PRIVILEGES;"

cd calcite_interface
mvn clean compile assembly:single
cd ..
