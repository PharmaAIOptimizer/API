import pandas as pd
import time
import mysql.connector

from db import getDBCursor, mydb
import json

def insertHistory(sessionCookie, number, w1, w2, w3, replacements, isMultiple=False):
    # Get the database cursor
    mycursor = getDBCursor()

    try:
        # Get user id from session cookie
        id = sessionCookie.split('-')[0]

        # SQL query to insert into search history
        query = "INSERT INTO historys (user_id, item_number, w_1, w_2, w_3, results, favorite, timestamp, isMultiple) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (id, number, w1, w2, w3, replacements, False, time.time(), isMultiple,)

        # Execute the SQL command
        mycursor.execute(query, values)

        # Commit the changes
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        mycursor.close()

def getHistory(sessionCookie):
    # Get the database cursor
    mycursor = getDBCursor()

    try:
        # Get user id from session cookie
        id = sessionCookie.split('-')[0]

        # SQL query to get search history
        query = "SELECT id, item_number, w_1, w_2, w_3, isMultiple, timestamp, results FROM historys WHERE user_id = %s"
        values = (id,)

        # Execute the SQL command
        mycursor.execute(query, values)

        # Fetch all the results
        result = mycursor.fetchall()

        return result

        # # Get the column names
        # columns = [desc[0] for desc in mycursor.description]

        # # Create a list of dictionaries, where each dictionary represents a row
        # data = []
        # for row in result:
        #     data.append(dict(zip(columns, row)))

        # # Convert the list of dictionaries to JSON
        # json_result = json.dumps(data)

        # return json_result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        mycursor.close()

def addToFavorites(sessionCookie, history_id):
    # Get the database cursor
    mycursor = getDBCursor()

    try:
        # Get user id from session cookie
        id = sessionCookie.split('-')[0]

        # SQL query to update the favorite column
        query = "UPDATE historys SET favorite = %s WHERE user_id = %s AND id = %s"
        values = (True, id, history_id,)

        # Execute the SQL command
        mycursor.execute(query, values)

        # Commit the changes
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        mycursor.close()

def removeFromFavorites(sessionCookie, history_id):
    # Get the database cursor
    mycursor = getDBCursor()

    try:
        # Get user id from session cookie
        id = sessionCookie.split('-')[0]

        # SQL query to update the favorite column
        query = "UPDATE historys SET favorite = %s WHERE user_id = %s AND id = %s"
        values = (False, id, history_id,)

        # Execute the SQL command
        mycursor.execute(query, values)

        # Commit the changes
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        mycursor.close()

def getFavorites(sessionCookie):
    # Get the database cursor
    mycursor = getDBCursor()

    try:
        # Get user id from session cookie
        id = sessionCookie.split('-')[0]

        # SQL query to get favorite history
        query = "SELECT id, item_number, w_1, w_2, w_3, isMultiple, timestamp, results FROM historys WHERE user_id = %s AND favorite = %s"
        values = (id, True,)

        # Execute the SQL command
        mycursor.execute(query, values)

        # Fetch all the results
        result = mycursor.fetchall()

        return result

        # # Get the column names
        # columns = [desc[0] for desc in mycursor.description]

        # # Create a list of dictionaries, where each dictionary represents a row
        # data = []
        # for row in result:
        #     data.append(dict(zip(columns, row)))

        # # Convert the list of dictionaries to JSON
        # json_result = json.dumps(data)

        # return json_result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        mycursor.close()
