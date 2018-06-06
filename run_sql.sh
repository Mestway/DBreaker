#bash

CALCITE_INTERFACE=calcite_interface/target/calcite_interface-1.0-SNAPSHOT.jar
DATABASE="test_db"
USER="dbtest"
PASSWORD="dbtest"

SQL_FILE="example/example.sql"
OUTPUT_CMD=""

if [ $# -ge 1 ]
  then
    SQL_FILE=$1
fi

if [ $# -ge 2 ]
  then
    OUTPUT_CMD="--output-file $2"
fi

echo $SQL_FILE
echo $OUTPUT_CMD

java -jar $CALCITE_INTERFACE --database $DATABASE --user $USER --password $PASSWORD --input-file $SQL_FILE $OUTPUT_CMD
