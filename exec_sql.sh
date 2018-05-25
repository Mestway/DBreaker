#bash

CALCITE_INTERFACE=calcite_interface/target/calcite_interface-1.0-SNAPSHOT.jar

java -jar $CALCITE_INTERFACE --database test_db --user dbtest --password dbtest --ddl calcite_interface/example/example.ddl.sql --query calcite_interface/example/example.sql
