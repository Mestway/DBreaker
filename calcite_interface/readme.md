# Calcite Interface

Executing SQL queries with Calcite and MySQL.

## Usage

Build calcite_interface.jar:

```
mvn clean compile assembly:single
```

Run the target query file: 

```
java -jar target/calcite_interface-1.0-SNAPSHOT.jar \
     --database DATABASE --user USERNAME --password PASSWORD\
     --input-file INPUT --output-file OUTPUT
```

