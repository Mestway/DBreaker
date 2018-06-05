# Calcite Interface

Executing SQL queries with Calcite and MySQL.

## Usage

Method 1 (Recommended): Build the jar file and run queries with the jar file:

```
mvn package
java -jar target/calcite_interface-1.0-SNAPSHOT.jar \
     --database test.db --user username --password password \
     --input-file input_file --output-file output_file
```