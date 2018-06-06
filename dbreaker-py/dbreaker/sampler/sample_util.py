import string
import random
from dbreaker.lang.sql import *
from dbreaker.lang.table import *

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
    {'op': '+' , 'input': ['NUMBER', 'NUMBER'], 'output': 'NUMBER', 'type': BinaryExpr },
    {'op': '-' , 'input': ['NUMBER', 'NUMBER'], 'output': 'NUMBER', 'type': BinaryExpr },
    {'op': '*' , 'input': ['NUMBER', 'NUMBER'], 'output': 'NUMBER', 'type': BinaryExpr },
    {'op': '/' , 'input': ['NUMBER', 'NUMBER'], 'output': 'NUMBER', 'type': BinaryExpr },
    #{'op': '%' , 'input': ['NUMBER', 'NUMBER'], 'output': 'NUMBER', 'type': BinaryExpr },
    #{'op': 'POWER' , 'input': ['NUMBER', 'NUMBER'], 'output': 'NUMBER', 'type': FunctionExpr },
    #{'op': 'ABS' , 'input': ['NUMBER'], 'output': 'NUMBER', 'type': FunctionExpr },
    {'op': '+' , 'input': ['NUMBER'], 'output': 'NUMBER', 'type': UnaryExpr },
    {'op': '-' , 'input': ['NUMBER'], 'output': 'NUMBER', 'type': UnaryExpr },

    # String Operators
    {'op': 'CHAR_LENGTH' , 'input': ['STRING'], 'output': 'NUMBER', 'type': FunctionExpr },
    {'op': 'UPPER' , 'input': ['STRING'], 'output': 'STRING', 'type': FunctionExpr },

    # Comparison Operators
    {'op': '=' , 'input': ['NUMBER', 'NUMBER'], 'output': 'BOOLEAN', 'type': BinaryExpr },
    {'op': '=' , 'input': ['STRING', 'STRING'], 'output': 'BOOLEAN', 'type': BinaryExpr },
    {'op': '<>' , 'input': ['NUMBER', 'NUMBER'], 'output': 'BOOLEAN', 'type': BinaryExpr },
    {'op': '!=' , 'input': ['NUMBER', 'NUMBER'], 'output': 'BOOLEAN', 'type': BinaryExpr },
    {'op': '>' , 'input': ['NUMBER', 'NUMBER'], 'output': 'BOOLEAN', 'type': BinaryExpr },
    {'op': '>=' , 'input': ['NUMBER', 'NUMBER'], 'output': 'BOOLEAN', 'type': BinaryExpr },
    {'op': '<' , 'input': ['NUMBER', 'NUMBER'], 'output': 'BOOLEAN', 'type': BinaryExpr },
    {'op': '<=' , 'input': ['NUMBER', 'NUMBER'], 'output': 'BOOLEAN', 'type': BinaryExpr },
    {'op': 'OR' , 'input': ['BOOLEAN', 'BOOLEAN'], 'output': 'BOOLEAN', 'type': BinaryExpr },
    {'op': 'AND' , 'input': ['BOOLEAN', 'BOOLEAN'], 'output': 'BOOLEAN', 'type': BinaryExpr },
]

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

# Generates a random string of uppercase letters of given length N
def sample_name(N):
    return ''.join(random.choices(string.ascii_uppercase, k=N))

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

def get_columns(tableSchema, types):
    columns = []
    for col in tableSchema.columns:
        matches = [s for s in types if str(col.ty).split("(")[0] in s]
        if (len(matches) > 0):
            columns.append(col)
    return columns