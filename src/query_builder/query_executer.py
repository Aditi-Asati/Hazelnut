from src.query_builder.db_connector import DBConnector, DBConnectionError


class QueryExecutionFailed(Exception):
    pass


def execute_query(query: str, dbconnection: DBConnector):
    try:
        connection = dbconnection.connect_to_db()

    except Exception:
        raise DBConnectionError("Couldn't connect to the database. Check credentials.")

    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except Exception as e:
        raise QueryExecutionFailed("Query execution failed.")
    result = cursor.fetchall()
    columns = cursor.column_names
    connection.close()
    return result, columns
