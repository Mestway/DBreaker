## Docker Setup

The docker is the environment for testing queries. If you don't have docker, you can install them following https://docs.docker.com/install/ To build the docker:

`docker build -t dbtest .`
`docker run -it dbtest`

Once you are inside the docker, you can run:

`./config_db.sh`

to initialize the database and the connector.

To test queries, run

`./exec_sql.sh [DDL_FILE.ddl.sql] [SQL_FILE.sql] [OUTPUT_FILE]`

Examples of DDL_FILE.ddl.sql and SQL_FILE.sql can be found in [calcite_interface/example](https://github.com/Mestway/dbreaker/tree/master/calcite_interface/example).

## Python Setup

In order to run query generator, you need to install the following python utils.

Install requirements

`pip install -r requirements.txt` or `conda install --file requirements.txt`

Install dbreaker in editable mode

`pip install -e .`
