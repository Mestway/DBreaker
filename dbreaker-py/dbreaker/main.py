import os, sys
import argparse
from dbreaker.sampler.generator import *

parser = argparse.ArgumentParser(description='Create some sample DDL and SQL queries')
parser.add_argument('--tables', '--t', dest='tables', type=int,
                   help='how many tables you want to produce', default=1)
parser.add_argument('--columns', '--c', dest='columns', type=int,
                   help='how many columns per table', default=1)
parser.add_argument('--selects', '--s', dest='selects', type=int,
                   help='how many select statements per table', default=1)

args = parser.parse_args()

# Generation code (in output files)
tables = args.tables
columns = args.columns
selects = args.selects

schemas = sample_schema(tables, columns)
for index, schema in enumerate(schemas):
    file = open(os.path.join(os.pardir, "output/query" + str(index + 1) + ".sql"), "w+")
    file.write(str(schema));
    file.write('\n\n')
    for i in range(0, selects):
        select = sample_select(schema)
        file.write(str(select))
        file.write('\n\n')
    file.close();    

