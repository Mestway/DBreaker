#bash

CALCITE_INTERFACE=calcite_interface/target/calcite_interface-1.0-SNAPSHOT.jar
DATABASE="test_db"
USER="dbtest"
PASSWORD="dbtest"

SQL_FILE="example/example.sql"
OUTPUT_CMD=""

echo $#

if [ $# -ge 2 ]
  then
    DDL_FILE=$1
    SQL_FILE=$2
fi

if [ $# -ge 3 ]
  then
    OUTPUT_CMD="--output-file $3"
fi

echo $SQL_FILE
echo $OUTPUT_CMD

java -jar $CALCITE_INTERFACE --database $DATABASE --user $USER --password $PASSWORD --input-file $SQL_FILE $OUTPUT_CMD
