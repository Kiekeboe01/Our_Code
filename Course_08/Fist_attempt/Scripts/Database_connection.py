import sqlite3


def connect_to_database(database_path):
    """
    Connects to the SQLite database using the provided database path.
    """
    con = sqlite3.connect(database_path)
    return con


def fetch_column_values(con, column_name):
    """
    Fetches values from the specified column in the database connection.
    """
    cur = con.cursor()
    if column_name == "keyword":
        # Join multiple tables to retrieve the column values for the specified column name
        cur.execute(f"SELECT K.{column_name} FROM Articles "
                    f"JOIN Articles_Keywords AK ON Articles.article_ID = AK.Articles_article_ID "
                    f"JOIN Keywords K ON K.keyword_ID = AK.Keywords_keyword_ID "
                    f"ORDER BY Articles.article_ID ASC;")
    else:
        # If the column name is not "keyword", simply retrieve the column values from the "Articles" table
        cur.execute(f"SELECT {column_name} FROM Articles;")
    values = cur.fetchall()
    return [value[0] for value in values]


def retrieve_column_values(column_name):
    """
    Retrieves column values from the specified database path and column name.
    """
    database_path = "../Python_Code/db_twinning.db"
    con = connect_to_database(database_path)
    values = fetch_column_values(con, column_name)
    con.close()
    return values
