import string
import random
from dbreaker.lang.sql import *
from dbreaker.lang.table import *

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

def get_columns_by_type(table_schema, types):
    columns = []
    for col in table_schema.columns:
        matches = [s for s in types if str(col.ty).split("(")[0] in s]
        if (len(matches) > 0):
            columns.append(col)
    return columns

# Numeric types for numeric expressions...
def filter_operators(table_schema, output_type):
    col_types = {
        'NUMBER': get_columns_by_type(table_schema, ColType.numeric_types),
        'BOOLEAN': get_columns_by_type(table_schema, ColType.boolean_types),
        'STRING': get_columns_by_type(table_schema, ColType.string_types)
    }
    available = []
    for key, value in col_types.items():
        if len(value) > 0:
            available.append(key)

    # Filter by output
    tmp = list(filter(lambda operator: operator['output'] == output_type, operators))
    # Filter by input, make sure our table_schema contains columns that can
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
    parse = random.choice(ColType.types).split('(')
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
        t = ColType(s_type, *params)
    else:
        t = ColType(s_type)
    return t

