import pandas as pd
import mysql.connector

from db import getDBCursor, mydb

def insertHistory(sessionCookie, number, w1, w2, w3, replacements):
    # Get the database cursor
    mycursor = getDBCursor()

    try:
        # Get user id from session cookie
        id = sessionCookie.split('-')[0]

        # SQL query to insert into search history
        query = "INSERT INTO historys (user_id, item_number, w_1, w_2, w_3, results, favorite) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (id, number, w1, w2, w3, replacements, False,)

        # Execute the SQL command
        mycursor.execute(query, values)

        # Commit the changes
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        mycursor.close()

