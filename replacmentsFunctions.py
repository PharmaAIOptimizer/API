import pandas as pd
import mysql.connector

from db import getDBCursor, mydb
from Analysis.ExactDrugAlgoFunction import ExactDrugAlgoFunction
from Analysis.getReplacements import getReplacements
from Analysis.CleanData import cleanData
from Analysis.AddPrice import addPriceAverage


def replacements(sessionCookie, number, isMultiple=False, w1=0.34, w2=0.33, w3=0.33):
    filename = 'Analysis/Daily Snapshot.csv'

    # Clean the data
    data_cleaned = cleanData(filename)

    # Similarity
    data, input = ExactDrugAlgoFunction(number, data_cleaned)

    # get replacements
    replacements = getReplacements(input, data, isMultiple)

    # Add the average price
    replacements = addPriceAverage(w1, w2, w3, replacements)

    # JSON format
    replacements = replacements.to_json(orient='records')

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

        # Return the replacements
        return replacements
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        mycursor.close()
