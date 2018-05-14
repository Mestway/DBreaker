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


# Operators ordered by associativity
# (https://en.wikipedia.org/wiki/Operator_associativity)
left_operators = ['.', '[]', '*', '/', '%', '+', '-',
                  '<', '>', '>=', '<=', '<>', '=', '!=',
                  'AND', 'OR']
right_operators = ['+', '-', 'NOT']
other_operators = ['BETWEEN', 'IN', 'LIKE', 'SIMILAR', 'OVERLAPS',
                   'CONTAINS', 'IS NULL', 'IS NOT NULL', 'IS FALSE']

def sample_expression(tableSchema):
    # TODO: Generate sample_expression (needs to be recursive and
    # use tableSchema columns)
    pass

# CREATE TABLE
def sample_schema(num_tables, num_columns):
    tableSchemas = []
    for i in range(0, num_tables):
        name = sample_name(7)
        columns = []
        for j in range(0, num_columns):
            columns.append(sample_column(0.2))
        tbl_constraint = sample_table_constraint(columns)
        table = TableSchema(name, columns, [tbl_constraint])
        # TODO: Table constraints
        tableSchemas.append(table)
    return tableSchemas

# Generates a random string of uppercase letters of given length N
def sample_name(N):
    return ''.join(random.choices(string.ascii_uppercase, k=N))

# Generates a table constraint given a list of column objects
def sample_table_constraint(columns):
    constraints = ['CHECK', 'PRIMARY KEY', 'UNIQUE']
    name = sample_name(5) if random.random() < 0.5 else ""
    constraint = random.choice(constraints)
    if (constraint == 'CHECK'):
        # exp = sample_expression()
        return TableConstraint(constraint, None, [], name)
    else:
        cols = [col.name for col in columns]
        cols = random.sample(cols, random.randint(1, len(cols)))
        return TableConstraint(constraint, None, cols, name)

# Given the name of a column, generate a constraint
def sample_col_constraint():
    nullCondition = "NOT" if random.random() < 0.5 else ""
    name = sample_name(5) if random.random() < 0 else ""
    return ColumnConstraint(name, nullCondition)


# p being the probability there is a constraint
def sample_column(p=0.0):
    name = sample_name(5)
    ty = sample_type()
    if (random.random() < p):
        constraint = sample_col_constraint()
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
                # TODO: For now, each type's parameters go from 0 - 30, but that needs to change
                params.append(random.randint(0, 30))
        t = Type(s_type, *params)
    else:
        t = Type(s_type)
    return t

for i in range(0, 100):
    for t in (sample_schema(3, 3)):
        print(t)
