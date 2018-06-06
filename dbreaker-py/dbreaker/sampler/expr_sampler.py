from dbreaker.lang.sql import *
from dbreaker.lang.table import *
from dbreaker.sampler.sample_util import *

def sample_expression(table_schema, ty, depth):
    # Based on the type we want generate that thing...
    if ty == 'BOOLEAN':
        return sample_boolean_expr(table_schema, depth)
    elif ty == 'NUMBER':
        return sample_numeric_expr(table_schema, depth)
    elif ty == 'STRING':
        return sample_string_expr(table_schema, depth)


def sample_numeric_expr(table_schema, depth):
    if depth == 0:
        # Return a number (include randomly generated numbers)
        num_columns = get_columns_by_type(table_schema, ColType.numeric_types)

        if (len(num_columns) == 0):
            return None
        else:
            c = random.choice(num_columns)
            return random.choice([random.randint(0, 10), table_schema.name + "." + c.name])
    else:
        number_operators = filter_operators(table_schema, 'NUMBER')
        op = random.choice(number_operators)
        params = []
        for p in op["input"]:
           params.append(sample_expression(table_schema, p, depth - 1))
        result = op["type"](op['op'], *params)
        return result


def sample_string_expr(table_schema, depth):
    if (depth == 0):
        # Return a string field...
        string_columns = get_columns_by_type(table_schema, ColType.string_types)
        if (len(string_columns) == 0):
            return None
        else:
            return table_schema.name + "." + random.choice(string_columns).name

    string_operators = filter_operators(table_schema, 'STRING')
    op = random.choice(string_operators)
    params = []
    for p in op["input"]:
       params.append(sample_expression(table_schema, p, depth - 1))
    result = op["type"](op['op'], *params)
    return result


def sample_boolean_expr(table_schema, depth):
    if (depth == 0):
        # Return a boolean field...
        boolean_columns = get_columns_by_type(table_schema, ColType.boolean_types)
        if (len(boolean_columns) == 0):
            return None
        else:
            return table_schema.name + "." + random.choice(boolean_columns).name

    boolean_operators = filter_operators(table_schema, 'BOOLEAN')
    op = random.choice(boolean_operators)
    params = []
    for p in op["input"]:
       params.append(sample_expression(table_schema, p, depth - 1))
    result = op["type"](op['op'], *params)
    return result