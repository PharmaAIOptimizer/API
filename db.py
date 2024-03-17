import mysql.connector

# Update the database connection details here
mydb = mysql.connector.connect(
  host="database-1.cx4iqu0qqry4.us-east-1.rds.amazonaws.com",
  database="postgres",  # Ensure this is the correct database name you intend to use
  user="postgres",
  password="seniordesign"
)

def getDBCursor():
    mycursor = mydb.cursor()
    mycursor.execute("USE postgres")  # Ensure this targets the correct database/schema
    return mycursor
