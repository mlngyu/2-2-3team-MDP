import mysql.connector

# Database credentials
host = '183.111.138.176'
user = 'imminho'
password = 'mu3102!!'
database = 'imminho'

# Create a connection
conn = mysql.connector.connect(host=host, user=user, password=password, database=database,port=3306)

# Create a cursor
cursor = conn.cursor()

# Your SQL queries go here
insert_query = "INSERT INTO test VALUES (%s)"
delete_query = "DELETE FROM test LIMIT 1"
cursor.execute(delete_query)
cursor.execute(insert_query, ('3',))
conn.commit()
# cursor.execute(insert_query, ('1',))

# Close the cursor and connection
cursor.close()
conn.close()