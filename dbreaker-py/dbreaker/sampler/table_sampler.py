from dbreaker.lang.table import *
from dbreaker.sampler.sample_util import *

import random

# Generates a table constraint given a list of column objects
def sample_table_constraint(tableSchema):
    constraints = ['CHECK', 'PRIMARY KEY', 'UNIQUE']
    name = sample_name(5) if random.random() < 0.5 else ""

    # There can only be one primary key at a time
    for constraint in tableSchema.tbl_constraints:
        if 'PRIMARY KEY' in constraints:
            constraints.remove('PRIMARY KEY')

    constraint = random.choice(constraints)
    if (constraint == 'CHECK'):
        exp = sample_boolean_expression(tableSchema, 1)
        return TableConstraint(constraint, exp, [], name)
    else:
        cols = [col.name for col in tableSchema.columns]
        cols = random.sample(cols, random.randint(1, len(cols)))
        return TableConstraint(constraint, None, cols, name)

# Given the name of a column, generate a constraint
def sample_col_constraint():
    nullCondition = "NOT " if random.random() < 0.5 else ""
    name = sample_name(5) if random.random() < 0 else ""
    return ColumnConstraint(name, nullCondition)

# p being the probability there is a constraint
def sample_column(p=0.0, name=None):
    if name is None:
        name = sample_name(5)
    ty = sample_type()
    if (random.random() < p):
        constraint = sample_col_constraint()
        return ColumnDef(name, ty, constraint)
    else:
        return ColumnDef(name, ty)

# CREATE TABLE
def sample_schema(num_tables, num_columns):
    tableSchemas = []
    for i in range(0, num_tables):
        name = "T" + str(i)
        columns = []
        for j in range(0, num_columns):
            columns.append(sample_column(0.2, "C" + str(j)))
        table = TableSchema(name, columns)
        if random.random() < 0.2:
            table.addConstraint(sample_table_constraint(table))
        # TODO: Table constraints
        tableSchemas.append(table)
    return tableSchemas