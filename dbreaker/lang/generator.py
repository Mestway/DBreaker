from dbreaker.lang.sql import *
from dbreaker.lang.table import *
import random
import string

# Potential SQL types
# n = length
# p = precision
# s = scale
# Array, Multiset, XML, INTERVAL, VARBINARY not supported on SQLfiddle...
# types = ['CHARACTER(n)', 'VARCHAR(n)', 'BINARY(n)',
#          'BOOLEAN', 'SMALLINT', 'INTEGER', 'BIGINT', 'DECIMAL(p, s)',
#          'NUMERIC(p, s)', 'FLOAT(p)', 'REAL', 'FLOAT', 'DOUBLE PRECISION',
#          'DATE', 'TIME', 'TIMESTAMP']
types = ['BOOLEAN', 'VARCHAR(n)', 'CHARACTER(n)', 'INTEGER', 'DECIMAL(p, s)']

# OPERATORS
math_operators = ['+', '-', '*', '/', '%']

function_operators = ['POWER(n, n)', 'ABS(n)']

unary_operators = ['-', '+']

comparison_operators = ['=', '<>', '!=', '>', '>=', '<', '<=']

logical_operators = ['OR', 'AND']

string_operators = ['CHAR_LENGTH(n)', 'UPPER(n)']
# Numeric types for numeric expressions...

def sample_expression(tableSchema, ty):
    # Based on the type we want generate that thing...
    if ty == 'BOOLEAN':
        return sample_boolean_expression(tableSchema)
    elif ty == 'NUMBER':
        return sample_num_expression(tableSchema)

def sample_boolean_expression(tableSchema):
    # Try number vs. number
    if len(get_num_columns(tableSchema)) > 0:
        left = sample_num_expression(tableSchema)
        right =  sample_num_expression(tableSchema)
        op = random.choice(comparison_operators)
        return ComparisonExpression(left, op, right)
    else:
        vals = ['NULL']
        boolean_compare = ['!=', '=']
        col = tableSchema.name + "." + random.choice(tableSchema.columns).name
        return ComparisonExpression(col, random.choice(boolean_compare), random.choice(vals))

# Helper function for grabbing columns of a certain type
def get_columns(tableSchema, types):
    columns = []
    for col in tableSchema.columns:
        matches = [s for s in types if str(col.ty).split("(")[0] in s]
        if (len(matches) > 0):
            columns.append(col)
    return columns

def get_num_columns(tableSchema):
    numeric_types = ['SMALLINT', 'INTEGER', 'BIGINT', 'NUMERIC(p, s)', 'DECIMAL(p, s)',
                     'FLOAT(p)', 'REAL', 'DOUBLE PRECISION']
    return get_columns(tableSchema, numeric_types)

def get_string_columns(tableSchema):
    boolean_types = ['BOOLEAN']
    return get_columns(tableSchema, boolean_types)

def get_boolean_columns(tableSchema):
    string_types = ['VARCHAR(n)', 'CHARACTER(n)']
    return get_columns(tableSchema, string_types)

def sample_num_expression(tableSchema):
    num_columns = get_num_columns(tableSchema)
    if (len(num_columns) == 0):
        # We can't do a number_expression... TODO: Figure out what to do here
        return None
    else:
        return number_expression(num_columns, 2, tableSchema.name)

def number_expression(cols, max_depth, tableName):
    # Return a boolean expression
    p = random.random()
    # Choose a random column
    c = random.choice(cols)

    if p < 0.25 or max_depth == 0:
        # Return a number (include randomly generated numbers)
        return random.choice([random.randint(0, 10), tableName + "." + c.name])
    elif p < 0.50:
        # Return a parenthesis
        n = number_expression(cols, max_depth - 1, tableName)
        return ParenthesizedExpression(n)
    elif p < 0.75:
        # Return a function expression
        f = random.choice(function_operators)
        args = f[f.find("(") + 1 : f.find(")")].count("n")
        op = f[:f.find("(")]
        number_args = []
        for i in range(0, args):
            number_args.append(number_expression(cols, max_depth - 1, tableName))
        return MathExpression(op, *number_args)
    else: 
        # Return an operation...
        left = number_expression(cols, max_depth - 1, tableName)
        right = number_expression(cols, max_depth - 1, tableName)
        op = random.choice(math_operators)
        return BinaryExpression(left, op, right)


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

# Generates a random string of uppercase letters of given length N
def sample_name(N):
    return ''.join(random.choices(string.ascii_uppercase, k=N))

# Generates a table constraint given a list of column objects
def sample_table_constraint(tableSchema):
    constraints = ['CHECK', 'PRIMARY KEY', 'UNIQUE']
    name = sample_name(5) if random.random() < 0.5 else ""

    # There can only be one primary key at a time
    for constraint in tableSchema.tbl_constraints:
        if 'PRIMARY KEY' in constraints:
            constraints.remove('PRIMARY KEY')

    print (tableSchema.tbl_constraints)
    constraint = random.choice(constraints)
    if (constraint == 'CHECK'):
        exp = sample_boolean_expression(tableSchema)
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

def sample_projection(tableSchema):
    cols = tableSchema.columns
    num_columns = random.randint(1, len(cols))
    if (num_columns == len(cols)):
        return "*"
    else:
        # Select random # columns (# being num_columns)
        random.shuffle(cols)
        cols = [c.name for c in cols[0:num_columns]]
        return ", ".join(map(str, cols))

def sample_select(tableSchema):
    # (self.options, self.proj_items, self.table_expr, self.where_pred)
    options = ['ALL', 'DISTINCT']
    option = ''
    if random.random() < 0.2:
        option = random.choice(options)
    proj_items = sample_projection(tableSchema)
    table_expr = tableSchema.name # for now... could have to use some alias stuff later on
    where_pred = sample_boolean_expression(tableSchema)
    return Select(option, proj_items, table_expr, where_pred, None, None, None)


# Generation code (in output files)
print("How many tables do you want?");
tables = int(input())
print("How many columns in the tables?");
columns = int(input())
print("How many select statements per table?");
selects = int(input())

schemas = sample_schema(tables, columns)
for index, schema in enumerate(schemas):
    file = open("output/query" + str(index + 1) + ".sql","w+")
    file.write(str(schema));
    file.write('\n\n')
    for i in range(0, selects):
        select = sample_select(schema)
        file.write(str(select))
        file.write('\n\n')
    file.close();    

