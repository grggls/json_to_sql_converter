import sqlparse


def validate_sql(query):
    try:
        sqlparse.parse(query)
        return True
    except sqlparse.exceptions.SQLParseError:
        return False
