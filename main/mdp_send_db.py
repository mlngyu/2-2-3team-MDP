import mysql.connector

def add_data_to_mariadb(host, user, password, database, data):
    try:
        # Establish a connection to the MariaDB server
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            print("Connected to MariaDB")

            # Create a cursor object to execute SQL queries
            cursor = connection.cursor()

            # Example table structure: (You need to adjust this based on your database schema)
            # CREATE TABLE IF NOT EXISTS your_table (id INT AUTO_INCREMENT PRIMARY KEY, data_column VARCHAR(255));

            # Example SQL query to insert data into the table
            insert_query = "INSERT INTO nucleof103 (temp) VALUES (%s)"

            cursor.execute(insert_query, (data,))

            # Commit the changes to the database
            connection.commit()

            print("Data added successfully")
            return 0

    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")

