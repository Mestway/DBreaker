import agate

# Potential SQL types
# n = length
# p = precision
# s = scale
# Array, Multiset, XML, INTERVAL, VARBINARY not supported on SQLfiddle...
# types = ['CHARACTER(n)', 'VARCHAR(n)', 'BINARY(n)',
#          'BOOLEAN', 'SMALLINT', 'INTEGER', 'BIGINT', 'DECIMAL(p, s)',
#          'NUMERIC(p, s)', 'FLOAT(p)', 'REAL', 'FLOAT', 'DOUBLE PRECISION',
#          'DATE', 'TIME', 'TIMESTAMP']

class ColType(object):

    types = ['BOOLEAN', 'VARCHAR(n)', 'CHARACTER(n)', 'INTEGER', 'DECIMAL(p, s)']

    numeric_types = ['SMALLINT', 'INTEGER', 'BIGINT', 
                     'NUMERIC(p, s)', 'DECIMAL(p, s)', 
                     'FLOAT(p)', 'REAL', 'DOUBLE PRECISION']
    boolean_types = ['BOOLEAN']
    string_types = ['VARCHAR(n)', 'CHARACTER(n)']

    def __init__(self, name, *params):
        self.name = name
        self.params = params

    def __str__(self):
        p_string = ",".join(map(str, self.params))
        if (p_string):
            p_string = "(" + p_string + ")"
        return self.name + p_string


class ColumnDef(object):

    def __init__(self, name, ty, col_constraint=None):
        self.name = name
        self.ty = ty
        self.col_constraint = col_constraint

    def __str__(self):
        if (self.col_constraint):
            return("%s %s %s" % (self.name, self.ty, self.col_constraint))
        else:
            return("%s %s" % (self.name, self.ty))


class ColumnConstraint(object):
    """
    columnConstraint:
          [ CONSTRAINT name ]
          [ NOT ] NULL
    """
    def __init__(self, name="", NOT=""):
        self.name = name
        self.NOT = NOT

    def __str__(self):
        if self.name:
            return "CONSTRAINT %s %s NULL" % (self.name, self.NOT)
        else:
            return "%sNULL" % (self.NOT)


class TableConstraint(object):
    """
    [ CONSTRAINT name ]
    {
        CHECK '(' expression ')'
    |   PRIMARY KEY '(' columnName [, columnName ]* ')'
    |   UNIQUE '(' columnName [, columnName ]* ')'
    }
    """
    def __init__(self, constraint, expression=None, columnNames=[], name=""):
        self.name = name
        self.constraint = constraint
        self.expression = expression
        self.columnNames = columnNames

    def __str__(self):
        if self.constraint == 'CHECK':
            return "%s (%s)" % (self.constraint, self.expression)
        else:
            col_string = ", ".join(self.columnNames)
            return "%s (%s)" % (self.constraint, col_string)


class TableSchema(object):

    def __init__(self, name, columns, tbl_constraints=[]):
        self.name = name
        self.columns = columns
        self.tbl_constraints = tbl_constraints  # table constraints

    def __str__(self):
        col_string = ", ".join(map(str, self.columns + self.tbl_constraints))
        return "CREATE TABLE %s (%s);" % (self.name, col_string)

    def addConstraint(self, constraint):
        self.tbl_constraints.append(constraint)


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
