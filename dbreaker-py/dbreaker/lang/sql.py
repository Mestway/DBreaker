import os

import copy
import dateutil
from pprint import pprint

# select:
#       SELECT [ STREAM ] [ ALL | DISTINCT ]
#           { * | projectItem [, projectItem ]* }
#       FROM tableExpression
#       [ WHERE booleanExpression ]
#       [ GROUP BY { groupItem [, groupItem ]* } ]
#       [ HAVING booleanExpression ]
#       [ WINDOW windowName AS windowSpec [, windowName AS windowSpec ]* ]
class Select(object):

    def __init__(self, options, proj_items, table_expr, 
                 where_pred, gb_items, having_pred, window):
        self.options = options
        self.proj_items = proj_items
        self.table_expr = table_expr
        self.where_pred = where_pred
        self.gb_items = gb_items
        self.having_pred = having_pred
        self.window = window

    def get_schema(self):
        return [f"c{i}" for i in range(len(self.vals))]

    # SELECT [OPTIONS] A, B, C, D
    # FROM [Table_expression]
    # WHERE [Boolean Expression]
    def __str__(self):
        # TODO: convert the tree to a string
        opt = ""
        if self.options != "":
            opt = str(self.options) + " "
        return ("SELECT %s%s\n"
                "FROM %s\n"
                "WHERE %s;") % (opt, self.proj_items, self.table_expr, self.where_pred)

# projectItem:
#       expression [ [ AS ] columnAlias ]
#   |   tableAlias . *
class ProjItem(object):

    def __init__(expr, alias):
        self.expr = expr
        self.alias = alias

    def __str__(self):
        if self.alias:
            # TODO: shouldn't AS be optional?
            return "%s AS %s" % (self.expr, self.alias)
        else:
            return "%s" % (self.expr)


# tableExpression:
#       tableReference [, tableReference ]*
#   |   tableExpression [ NATURAL ] [ ( LEFT | RIGHT | FULL ) [ OUTER ] ] 
#            JOIN tableExpression [ joinCondition ]
#   |   tableExpression CROSS JOIN tableExpression
#   |   tableExpression [ CROSS | OUTER ] APPLY tableExpression
class TableRefList(object):

    def __init__(self, table_refs):
        self.table_refs = table_refs

    def __str__(self):
        # TODO: convert the tree to a string
        pass


class JoinExp(object):
    # include the latter three tableExp
    def __init__(self, table_expr1, join_op, table_expr2, join_cond):
        self.table_expr1 = table_expr1
        self.join_op = join_op
        self.table_expr2 = table_expr2
        self.join_cond = join_cond

    def __str__(self):
        # TODO: convert the tree to a string
        pass


# joinCondition:
#       ON booleanExpression
#   |   USING '(' column [, column ]* ')'
class UsingExp(object):
    def __init__(self, columns):
        self.columns = columns

    def __str__(self):
        # TODO: convert the tree to a string
        pass


# tableReference:
#       tablePrimary
#       [ matchRecognize ]
#       [ [ AS ] alias [ '(' columnAlias [, columnAlias ]* ')' ] ]
# tablePrimary:
#       [ [ catalogName . ] schemaName . ] tableName
#       '(' TABLE [ [ catalogName . ] schemaName . ] tableName ')'
#   |   tablePrimary [ EXTEND ] '(' columnDecl [, columnDecl ]* ')'
#   |   [ LATERAL ] '(' query ')'
#   |   UNNEST '(' expression ')' [ WITH ORDINALITY ]
#   |   [ LATERAL ] TABLE '(' [ SPECIFIC ] functionName '(' expression [, expression ]* ')' ')'
class TableRef(object):
    # we current restrict tablePrimary to direct table reference only
    def __init__(self, table, alias, column_alias=None):
        self.table = table
        self.alias = alias
        self.column_alias = column_alias

    def __str__(self):
        # TODO: convert the tree to a string
        pass


# selectWithoutFrom:
#       SELECT [ ALL | DISTINCT ]
#           { * | projectItem [, projectItem ]* }
class SelectWithoutFrom(object):

    def __init__(self, option, proj_items):
        self.option = option
        self.proj_items = proj_items

    def __str__(self):
        # TODO: convert the tree to a string
        pass


# groupItem:
#       expression
#   |   '(' ')'
#   |   '(' expression [, expression ]* ')'
#   |   CUBE '(' expression [, expression ]* ')'
#   |   ROLLUP '(' expression [, expression ]* ')'
#   |   GROUPING SETS '(' groupItem [, groupItem ]* ')'
class GroupItem(object):

    def __init__(self, option, expr_list):
        self.option = option
        self.expr_list = expr_list

    def __str__(self):
        # TODO: convert the tree to a string
        pass


# windowRef:
#       windowName
#   |   windowSpec

# windowSpec:
#       [ windowName ]
#       '('
#       [ ORDER BY orderItem [, orderItem ]* ]
#       [ PARTITION BY expression [, expression ]* ]
#       [
#           RANGE numericOrIntervalExpression { PRECEDING | FOLLOWING }
#       |   ROWS numericExpression { PRECEDING | FOLLOWING }
#       ]
#       ')'
class WindowRef(object):
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def __str__(self):
        # TODO: convert the tree to a string
        pass


class WindowBody(object):
    def __init__(self, name, order_item, partition_expr):
        self.name = name
        self.order_item = order_item
        self.partition_expr = partition_expr

    def __str__(self):
        # TODO: convert the tree to a string
        pass

# =============== Expressions and predicates =================

class ColRef(object):

    def __init__(self, col_name):
        self.col_name = col_name

    def __str__(self):
        # TODO: convert the tree to a string
        pass


class Const(object):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        # TODO: convert the tree to a string
        pass


class Expr(object):
    # expression includes boolean expression, 
    # numeric expression, aggregation expression, and interval expression
    def __init__(self, op, vals):
        self.op = op
        self.vals = vals

    def __str__(self):
        # TODO: convert the tree to a string
        pass

class Expression:
    pass

class BinaryExpression(Expression):
    def __init__(self, op, left, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return "(%s %s %s)" % (self.left, self.op, self.right)

class UnaryExpression(Expression):
    # +Right or -Right
    def __init__(self, op, right):
        self.op = op
        self.right = right

    def __str__(self):
        return "%s%s" % (self.op, self.right)

class FunctionExpression(Expression):
    # COS(3) or MOD(5, 3)
    def __init__(self, op, *args):
        self.op = op
        self.args = args

    def __str__(self):
        arg_str = ", ".join(map(str, self.args))
        return "%s(%s)" % (self.op, arg_str)
