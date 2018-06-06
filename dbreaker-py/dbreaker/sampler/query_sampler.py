from dbreaker.lang.sql import *
from dbreaker.lang.table import *
from dbreaker.sampler.sample_util import *
from dbreaker.sampler.table_sampler import *
import random

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
