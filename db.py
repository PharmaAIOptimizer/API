import psycopg2

mydb = psycopg2.connect(database = "Users", 
                        user = "postgres", 
                        host= 'database-1.cx4iqu0qqry4.us-east-1.rds.amazonaws.com',
                        password = "seniordesign",
                        port = 5432)

def getDBCursor():
    mycursor = mydb.cursor()
    return mycursor