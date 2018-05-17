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
# left_operators = ['.', '[]', '*', '/', '%', '+', '-',
#                   '<', '>', '>=', '<=', '<>', '=', '!=',
#                   'AND', 'OR']
# right_operators = ['+', '-', 'NOT']
# other_operators = ['BETWEEN', 'IN', 'LIKE', 'SIMILAR', 'OVERLAPS',
#                    'CONTAINS', 'IS NULL', 'IS NOT NULL', 'IS FALSE']

math_operators = ['+', '-', '*', '/', '%']

function_operators = ['POWER(n, n)', 'ABS(n)', 'MOD(n, n)', 'SQRT(n)', 'LN(n)',
                      'LOG10(n)', 'EXP(n)', 'CEIL(n)', 'FLOOR(n)', 'RAND()',
                      'RAND_INTEGER(n)', 'ACOS(n)', 'ASIN(n)', 'ATAN(n)',
                      'ATAN2(n, n)', 'COS(n)', 'COT(n)', 'DEGREES(n)', 'RADIANS(n)',
                      'ROUND(n)', 'ROUND(n, n)', 'SIGN(n)', 'SIN(n)', 'TAN(n)',
                      'TRUNCATE(n)', 'TRUNCATE(n, n)', 'PI()']
unary_operators = ['-', '+']

# Numeric types for numeric expressions...
numeric_types = ['SMALLINT', 'INTEGER', 'BIGINT', 'NUMERIC(p, s)', 'DECIMAL(p, s)',
                 'FLOAT(p)', 'REAL', 'DOUBLE PRECISION']

def sample_expression(tableSchema):
    # TODO: Generate sample_expression (needs to be recursive and
    # use tableSchema columns)
    pass

def sample_num_expression(tableSchema):
    num_columns = []
    for col in tableSchema.columns:
        matches = [s for s in numeric_types if str(col.ty) in s]
        if (len(matches) > 0):
            num_columns.append(col)
    if (len(num_columns) == 0):
        # We can't do a number_expression... TODO: Figure out what to do here
        return None
    else:
        return number_expression(num_columns, 5)

def number_expression(cols, max_depth):
    # Return a boolean expression
    p = random.random()
    # Choose a random column
    c = random.choice(cols)

    if p < 0.25 or max_depth == 0:
        # Return a number (include randomly generated numbers)
        if (c is None):
            return random.randint(0, 10)
        else:
            return random.choice([random.randint(0, 10), c.name])
    elif p < 0.50:
        # Return a parenthesis
        n = number_expression(cols, max_depth - 1)
        return ParenthesizedExpression(n)
    elif p < 0.75:
        # Return a function expression
        f = random.choice(function_operators)
        args = f[f.find("(") + 1 : f.find(")")].count("n")
        op = f[:f.find("(")]
        number_args = []
        for i in range(0, args):
            number_args.append(number_expression(cols, max_depth - 1))
        return MathExpression(op, *number_args)
    else: 
        # Return an operation...
        left = number_expression(cols, max_depth - 1)
        right = number_expression(cols, max_depth - 1)
        op = random.choice(math_operators)
        return BinaryExpression(left, op, right)


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

test = None 
for i in range(0, 100):
    for t in (sample_schema(3, 3)):
        print(t)
        test = t

print(test)
print(sample_num_expression(test))

