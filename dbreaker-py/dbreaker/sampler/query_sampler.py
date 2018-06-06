from dbreaker.lang.sql import *
from dbreaker.lang.table import *
from dbreaker.sampler.sample_util import *
from dbreaker.sampler.table_sampler import *
import random


def sample_projection(table_schema):
    cols = table_schema.columns
    num_columns = random.randint(1, len(cols))
    if (num_columns == len(cols)):
        return "*"
    else:
        # Select random # columns (# being num_columns)
        random.shuffle(cols)
        cols = [c.name for c in cols[0:num_columns]]
        return ", ".join(map(str, cols))

def sample_select(table_schema):
    # (self.options, self.proj_items, self.table_expr, self.where_pred)
    options = ['ALL', 'DISTINCT']
    option = ''
    if random.random() < 0.2:
        option = random.choice(options)
    proj_items = sample_projection(table_schema)
    table_expr = table_schema.name # for now... could have to use some alias stuff later on
    where_pred = sample_boolean_expr(table_schema, 3)
    return Select(option, proj_items, table_expr, where_pred, None, None, None)
