import agate

class Type(object):

    def __init__(self, name, *params):
        self.name = name
        self.params = params

    def __str__(self):
        p_string = ",".join(map(str, self.params))
        if (p_string):
            p_string = "(" + p_string + ")"
        return self.name + p_string

class ColumnDef(object):

    def __init__(self, name, ty, col_constraint):
        self.name = name
        self.ty = ty
        self.col_constraint = col_constraint


class TableSchema(object):

    def __init__(self, name, columns, tbl_constraint):
        self.name = name
        self.columns = columns
        self.tbl_constraint = tbl_constraint # table constraints
        

class Table(object):

    def __init__(self, schema, content):
        """ Args:
                schema: the table schema definition
                content: a list of tuples storing the table content
        """
        self.schema = schema
        self.content = content

    @staticmethod
    def load_from_csv(schema, filename):
        ''' Create a table from an agate table,
            data content and datatypes are based on how agate interprets them
        '''
        table_name = os.path.basename(filename).split(".")[0]

        agate_table = agate.Table.from_csv(filename)

        # store the table into a list
        content = []
        for row in agate_table.rows:
            row_content = []
            for j, c in enumerate(row):
                row_content.append(c)
            content.append(tuple(row_content))

        return Table(schema, content)

    def __str__(self):
        s = f'{str(self.schema)}\n'
        s += "\n".join([", ".join([str(x) for x in r]) for r in self.content])
        return s