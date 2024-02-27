import uuid
import time
import mysql.connector

from db import getDBCursor, mydb
from userFunctions import get_user_data_by_name, verify_password_bcrypt

def generate_session_cookie(id):
    session_cookie = str(uuid.uuid4())
    session_cookie = str(id) + '-' + session_cookie
    timestamp = int(time.time())
    return session_cookie, timestamp

# Insert session cookie and timestamp into the database
def insert_session_cookie(user_id, session_cookie, timestamp):
    # Get the database cursor
    mycursor = getDBCursor()
    
    try:
        # SQL query to insert session cookie and timestamp
        query = "UPDATE users SET session_cookie = %s, session_cookie_timestamp = %s WHERE id = %s"
        values = (session_cookie, timestamp, user_id)
        
        # Execute the SQL command
        mycursor.execute(query, values)
        
        # Commit the changes
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        mycursor.close()

# Login function
def login(username, password):
    user_data = get_user_data_by_name(username)
    
    if user_data:
        if verify_password_bcrypt(user_data['password'], password):
            session_cookie, timestamp = generate_session_cookie(user_data['id'])
            user_id = user_data['id']
            insert_session_cookie(user_id, session_cookie, timestamp)
            return session_cookie, timestamp
        else:
            print("Invalid password.")
            return None
    else:
        print("User not found.")
        return None
    
# Check db if the session cookie is valid
def is_session_cookie_valid(session_cookie):
    # Get the database cursor
    mycursor = getDBCursor()
    
    try:
        # SQL query to get user by session cookie and timestamp
        query = "SELECT * FROM users WHERE session_cookie = %s"
        values = (session_cookie,)
        
        # Execute the SQL command
        mycursor.execute(query, values)
        
        # Fetch the result
        result = mycursor.fetchone()
        
        if result and int(time.time()) - result[5] < 3600:
            print("Session cookie is valid.")
            return True
        else:
            print("Session cookie is invalid or expired.")
            return False
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        mycursor.close()

# Logout function
def logout(session_cookie):
    # Get the database cursor
    mycursor = getDBCursor()
    
    try:
        # SQL query to delete session cookie and timestamp
        query = "UPDATE users SET session_cookie = '', session_cookie_timestamp = 0 WHERE session_cookie = %s"
        values = (session_cookie,)
        
        # Execute the SQL command
        mycursor.execute(query, values)
        
        # Commit the changes
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        mycursor.close()
