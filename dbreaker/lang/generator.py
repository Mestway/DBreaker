from dbreaker.lang.sql import *
from dbreaker.lang.table import *
import random

def sample_schema(num_tables, num_columns):
    pass

# n = length
# p = precision
# s = scale

# Potential SQL types
types = ['CHARACTER(n)', 'VARCHAR(n)', 'BINARY(n)', 'VARBINARY(n)',
         'BOOLEAN', 'SMALLINT', 'INTEGER', 'BIGINT', 'DECIMAL(p, s)',
         'NUMERIC(p, s)', 'FLOAT(p)', 'REAL', 'FLOAT', 'DOUBLE PRECISION',
         'DATE', 'TIME', 'TIMESTAMP', 'INTERVAL', 'ARRAY', 'MULTISET', 'XML']

# Returns a list of the number of types you want for a table...
def sample_type(num_types):
    types = []
    for i in range(0, num_types):
        parse = random.choice(types).split('(')
        s_type = parse[0]
        # That means there are parameters we have to consider
        if (len(parse) > 1):
            param_list = parse[1][:-1].split(',')
            params = []
            for p in param_list:
                # TODO: Generate a specific num for n, p or s?
                params.append(random.randint(0, 255))
            t = Type(s_type, *params)
        else:
            t = Type(s_type)
        types.append(t)
    return types
