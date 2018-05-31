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

operators = [
    # Number Operators
    {'op': '+' , 'input': ['NUMBER', 'NUMBER'], 'output': 'NUMBER', 'type': BinaryExpression },
    {'op': '-' , 'input': ['NUMBER', 'NUMBER'], 'output': 'NUMBER', 'type': BinaryExpression },
    {'op': '*' , 'input': ['NUMBER', 'NUMBER'], 'output': 'NUMBER', 'type': BinaryExpression },
    {'op': '/' , 'input': ['NUMBER', 'NUMBER'], 'output': 'NUMBER', 'type': BinaryExpression },
    {'op': '%' , 'input': ['NUMBER', 'NUMBER'], 'output': 'NUMBER', 'type': BinaryExpression },
    {'op': 'POWER' , 'input': ['NUMBER', 'NUMBER'], 'output': 'NUMBER', 'type': FunctionExpression },
    {'op': 'ABS' , 'input': ['NUMBER'], 'output': 'NUMBER', 'type': FunctionExpression },
    {'op': '+' , 'input': ['NUMBER'], 'output': 'NUMBER', 'type': UnaryExpression },
    {'op': '-' , 'input': ['NUMBER'], 'output': 'NUMBER', 'type': UnaryExpression },

    # String Operators
    {'op': 'CHAR_LENGTH' , 'input': ['STRING'], 'output': 'NUMBER', 'type': FunctionExpression },
    {'op': 'UPPER' , 'input': ['STRING'], 'output': 'STRING', 'type': FunctionExpression },

    # Comparison Operators
    {'op': '=' , 'input': ['NUMBER', 'NUMBER'], 'output': 'BOOLEAN', 'type': BinaryExpression },
    {'op': '=' , 'input': ['STRING', 'STRING'], 'output': 'BOOLEAN', 'type': BinaryExpression },
    {'op': '<>' , 'input': ['NUMBER', 'NUMBER'], 'output': 'BOOLEAN', 'type': BinaryExpression },
    {'op': '!=' , 'input': ['NUMBER', 'NUMBER'], 'output': 'BOOLEAN', 'type': BinaryExpression },
    {'op': '>' , 'input': ['NUMBER', 'NUMBER'], 'output': 'BOOLEAN', 'type': BinaryExpression },
    {'op': '>=' , 'input': ['NUMBER', 'NUMBER'], 'output': 'BOOLEAN', 'type': BinaryExpression },
    {'op': '<' , 'input': ['NUMBER', 'NUMBER'], 'output': 'BOOLEAN', 'type': BinaryExpression },
    {'op': '<=' , 'input': ['NUMBER', 'NUMBER'], 'output': 'BOOLEAN', 'type': BinaryExpression },
    {'op': 'OR' , 'input': ['BOOLEAN', 'BOOLEAN'], 'output': 'BOOLEAN', 'type': BinaryExpression },
    {'op': 'AND' , 'input': ['BOOLEAN', 'BOOLEAN'], 'output': 'BOOLEAN', 'type': BinaryExpression },
]

# Numeric types for numeric expressions...
def filter_operators(tableSchema, output):
    col_types = {
        'NUMBER': get_num_columns(tableSchema),
        'BOOLEAN': get_boolean_columns(tableSchema),
        'STRING': get_string_columns(tableSchema)
    }
    available = []
    for key, value in col_types.items():
        if len(value) > 0:
            available.append(key)

    # Filter by output
    tmp = list(filter(lambda operator: operator['output'] == output, operators))
    # Filter by input, make sure our tableSchema contains columns that can
    # go into these expressions
    result = []
    for v in tmp:
        ok = True
        for i in v['input']:
            if i not in available:
                ok = False
                break
        if ok:
            result.append(v)
    return result

def sample_expression(tableSchema, ty, depth):
    # Based on the type we want generate that thing...
    if ty == 'BOOLEAN':
        return sample_boolean_expression(tableSchema, depth)
    elif ty == 'NUMBER':
        return sample_num_expression(tableSchema, depth)
    elif ty == 'STRING':
        return sample_string_expression(tableSchema, depth)

def sample_num_expression(tableSchema, depth):
    if depth == 0:
        # Return a number (include randomly generated numbers)
        num_columns = get_num_columns(tableSchema)
        if (len(num_columns) == 0):
            return None
        else:
            c = random.choice(num_columns)
            return random.choice([random.randint(0, 10), tableSchema.name + "." + c.name])
    else:
        number_operators = filter_operators(tableSchema, 'NUMBER')
        op = random.choice(number_operators)
        params = []
        for p in op["input"]:
           params.append(sample_expression(tableSchema, p, depth - 1))
        result = op["type"](op['op'], *params)
        return result

def sample_string_expression(tableSchema, depth):
    if (depth == 0):
        # Return a string field...
        string_columns = get_string_columns(tableSchema)
        if (len(string_columns) == 0):
            return None
        else:
            return tableSchema.name + "." + random.choice(string_columns).name

    string_operators = filter_operators(tableSchema, 'STRING')
    op = random.choice(string_operators)
    params = []
    for p in op["input"]:
       params.append(sample_expression(tableSchema, p, depth - 1))
    result = op["type"](op['op'], *params)
    return result

def sample_boolean_expression(tableSchema, depth):
    if (depth == 0):
        # Return a boolean field...
        boolean_columns = get_boolean_columns(tableSchema)
        if (len(boolean_columns) == 0):
            return None
        else:
            return tableSchema.name + "." + random.choice(boolean_columns).name

    boolean_operators = filter_operators(tableSchema, 'BOOLEAN')
    op = random.choice(boolean_operators)
    params = []
    for p in op["input"]:
       params.append(sample_expression(tableSchema, p, depth - 1))
    result = op["type"](op['op'], *params)
    return result

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

def get_boolean_columns(tableSchema):
    boolean_types = ['BOOLEAN']
    return get_columns(tableSchema, boolean_types)

def get_string_columns(tableSchema):
    string_types = ['VARCHAR(n)', 'CHARACTER(n)']
    return get_columns(tableSchema, string_types)

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
    where_pred = sample_boolean_expression(tableSchema, 3)
    return Select(option, proj_items, table_expr, where_pred, None, None, None)
