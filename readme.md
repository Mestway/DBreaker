## Project Structure

* `calcite_interface/`: (java) code for running calcite on top of mysql.
* `dbreaker-py/`: (python) code for sampling and mutating SQL queries.

## Docker Setup

The docker is the environment for testing queries. If you don't have docker, you can install them following https://docs.docker.com/install/ To build the docker:

`docker build -t dbtest .`

`docker run -it dbtest`

Once you are inside the docker, you can run:

`./config_db.sh`

to initialize the database and the connector.

To test queries, run

`./run_sql.sh [DDL_FILE.ddl.sql] [SQL_FILE.sql] [OUTPUT_FILE]`

Examples of DDL_FILE.ddl.sql and SQL_FILE.sql can be found in [calcite_interface/example](https://github.com/Mestway/dbreaker/tree/master/example).

## Python Setup

Required Python Version: 3.6 

(Peplace `pip` and `python` with `pip3` and `python3` if Python 3.6 is not your default python in the following commands)

In order to run query generator, you need to install the following python utils.

Install requirements

`pip install -r requirements.txt` or `conda install --file requirements.txt`

Install dbreaker in editable mode

`pip install -e .`

Run Generator

`python main.py --tables 5 --columns 5 --selects 5`

This command generates 5 seperate query files each containing a create table statement
of a table with 5 columns along with 5 selects to go with it.

## Related Work

http://vldb.org/conf/2007/papers/industrial/p1243-bati.pdf
