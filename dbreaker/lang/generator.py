from dbreaker.lang.sql import *
from dbreaker.lang.table import *
import random
import string

# Potential SQL types
# n = length
# p = precision
# s = scale
# Array, Multiset, XML, INTERVAL, VARBINARY not supported on SQLfiddle...
types = ['CHARACTER(n)', 'VARCHAR(n)', 'BINARY(n)',
         'BOOLEAN', 'SMALLINT', 'INTEGER', 'BIGINT', 'DECIMAL(p, s)',
         'NUMERIC(p, s)', 'FLOAT(p)', 'REAL', 'FLOAT', 'DOUBLE PRECISION',
         'DATE', 'TIME', 'TIMESTAMP']

# Potential column constraints
col_constraints = ['NOT NULL', 'UNIQUE']

# Potential table constraints
table_constraints = ['PRIMARY KEY', 'UNIQUE', 'DEFAULT', 'CHECK']


# CREATE TABLE
def sample_schema(num_tables, num_columns):
    tableSchemas = []
    for i in range(0, num_tables):
        name = sample_name(7)
        columns = []
        for j in range(0, num_columns):
            columns.append(sample_column(0.2))
        table = TableSchema(name, columns)
        # TODO: Table constraints
        tableSchemas.append(table)
    return tableSchemas


# Generates a random string of uppercase letters of given length N
def sample_name(N):
    return ''.join(random.choices(string.ascii_uppercase, k=N))


def sample_constraint():
    return random.choice(col_constraints)


# p being the probability there is a constraint
def sample_column(p=0.0):
    name = sample_name(5)
    ty = sample_type()
    if (random.random() < p):
        constraint = sample_constraint()
        return ColumnDef(name, ty, constraint)
    else:
        return ColumnDef(name, ty)


# Returns a list of the number of types you want for a table...
def sample_type():
    parse = random.choice(types).split('(')
    s_type = parse[0]
    # That means there are parameters we have to consider
    if (len(parse) > 1):
        param_list = parse[1][:-1].split(',')
        params = []
        for p in param_list:
            # TODO: p (precision) has to be greater or equal to s (scale)
            p = p.strip()
            if p == 's':
                params.append(random.randint(0, params[len(params) - 1]))
            else:
                params.append(random.randint(0, 30))
        t = Type(s_type, *params)
    else:
        t = Type(s_type)
    return t

for i in range(0, 100):
    for t in (sample_schema(3, 3)):
        print(t)
