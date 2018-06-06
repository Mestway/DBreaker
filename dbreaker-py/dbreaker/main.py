import os, sys
import argparse
from pprint import pprint
from dbreaker.sampler.query_sampler import *
from dbreaker.sampler.table_sampler import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create some sample DDL and SQL queries')
    parser.add_argument('--ntables', '-t', dest='ntables', type=int,
                       help='the number of tables used', default=1)
    parser.add_argument('--ncolumns', '-c', dest='ncolumns', type=int,
                       help='the number of columns for each table', default=3)
    parser.add_argument('--nqueries', '-q', dest='nqueries', type=int,
                       help='the number of select queries for each table', default=5)
    parser.add_argument('--output-file', '-o', dest="output_file", type=str, help='output file', default=None)

    args = parser.parse_args()

    # Generation code (in output files)
    ntables = args.ntables
    ncolumns = args.ncolumns
    nqueries = args.nqueries
    output_file = args.output_file

    # output file / stdout
    f = sys.stdout if output_file is None else open(output_file, "w+")

    schemas = sample_schema(ntables, ncolumns)
    queries = [sample_select(schemas[0])]

    f.write('---------- [DDL]\n')
    for schema in schemas:
        f.write(str(schema) + "\n");

    f.write('\n---------- [Queries]\n')
    for q in queries:
        f.write(str(q) + "\n")

    f.close();