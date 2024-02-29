import mysql.connector
import hashlib
import os
import base64

from db import getDBCursor, mydb

def hash_password_sha256(password):
    """Hash a password for storing using SHA-256 and a random salt, storing the hash and salt as base64-encoded strings."""
    salt = os.urandom(32)  # Generate a 32-byte random salt
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    # Encode the salt and hash as base64 to get strings
    salt_str = base64.b64encode(salt).decode('utf-8')
    pwdhash_str = base64.b64encode(pwdhash).decode('utf-8')
    # Concatenate salt and hash as strings with a separator
    storage = salt_str + '$' + pwdhash_str
    return storage

def verify_password_sha256(stored_password, provided_password):
    """Verify a stored password (stored as a base64-encoded string) against one provided by user using SHA-256."""
    # Split the stored_password string into salt and hash components
    salt_str, stored_hash_str = stored_password.split('$')
    # Decode the salt and hash from base64
    salt = base64.b64decode(salt_str)
    stored_hash = base64.b64decode(stored_hash_str)
    # Hash the provided_password using the extracted salt and compare
    pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return pwdhash == stored_hash

# Example usage:
#hashed_bcrypt = hash_password_sha256('secure_password')
#print(verify_password_sha256(hashed_bcrypt, 'secure_password'))  # This will return True if the password matches

# Function to create a new user
def create_user(username, password, center, permission, employeeid, islocked):
    # Get the database cursor
    mycursor = getDBCursor()
    
    try:
        # Hash the password
        password = hash_password_sha256(password)
        # SQL query to insert a new user
        query = "INSERT INTO users (username, password, center, permission, employeeid, islocked) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (username, password, center, permission, employeeid, islocked,)
        
        # Execute the SQL command
        mycursor.execute(query, values)
        
        # Commit the changes to the database
        mydb.commit()
        
        print("User created successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        mycursor.close()

# Example usage:
#create_user('Manu', 'pass', 'user@example.com')
        
# Function to get a user by username
def get_user_data_by_name(username):
    # Get the database cursor
    mycursor = getDBCursor()
    
    try:
        # SQL query to get a user by username
        query = "SELECT * FROM users WHERE username = %s"
        values = (username,)
        
        # Execute the SQL command
        mycursor.execute(query, values)
        
        # Fetch the result
        result = mycursor.fetchone()
        
        if result:
            return {
                "id": result[0],
                "username": result[1],
                "password": result[2],
                "center": result[3],
                "permission": result[4],
                "employeeid": result[5],
                "islocked": result[6],
                "session_cookie": result[7],
                "session_cookie_timestamp": result[8],
            }
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        mycursor.close()

# Example usage:
#print(get_user_data_by_name('Manu'))  # This will return the user data if the user exists
        
# Function to get a user by id
def get_user_data_by_id(id):
    # Get the database cursor
    mycursor = getDBCursor()
    
    try:
        # SQL query to get a user by id
        query = "SELECT * FROM users WHERE id = %s"
        values = (id,)
        
        # Execute the SQL command
        mycursor.execute(query, values)
        
        # Fetch the result
        result = mycursor.fetchone()
        
        if result:
            return {
                "id": result[0],
                "username": result[1],
                "password": result[2],
                "center": result[3],
                "permission": result[4],
                "employeeid": result[5],
                "islocked": result[6],
                "session_cookie": result[7],
                "session_cookie_timestamp": result[8],
            }
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        mycursor.close()

# Example usage:
#print(get_user_data_by_id(1))  # This will return the user data if the user exists
        
# Function to delete a user by id
def delete_user(id):
    # Get the database cursor
    mycursor = getDBCursor()
    
    try:
        # SQL query to delete a user by id
        query = "DELETE FROM users WHERE id = %s"
        values = (id,)
        
        # Execute the SQL command
        mycursor.execute(query, values)
        
        # Commit the changes to the database
        mydb.commit()
        
        print("User deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        mycursor.close()

# Example usage:
#delete_user(1)  # This will delete the user with id 1
