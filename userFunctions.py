import mysql.connector
import bcrypt
from db import getDBCursor, mydb

def hash_password_bcrypt(password):
    """Hash a password for storing."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password_bcrypt(stored_password_hash, provided_password):
    """Verify a stored password against one provided by user."""
    # Ensure stored_password_hash is in byte format
    if isinstance(stored_password_hash, str):
        stored_password_hash = stored_password_hash.encode('utf-8')
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password_hash)

# Example usage:
#hashed_bcrypt = hash_password_bcrypt('secure_password')
#print(verify_password_bcrypt(hashed_bcrypt, 'secure_password'))  # This will return True if the password matches

# Function to create a new user
def create_user(username, password, email):
    # Get the database cursor
    mycursor = getDBCursor()
    
    try:
        # Hash the password
        password = hash_password_bcrypt(password)
        # SQL query to insert a new user
        query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        values = (username, password, email)
        
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
                "email": result[3],
                "session_cookie": result[4],
                "session_cookie_timestamp": result[5]
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
                "email": result[3],
                "session_cookie": result[4],
                "session_cookie_timestamp": result[5]
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
