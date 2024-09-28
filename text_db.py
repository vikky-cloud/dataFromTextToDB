import mysql.connector
import os

# Get DB config from the user
def get_db_config():
    print("Enter your database configuration details:")
    user = input("Username: ")
    password = input("Password: ")
    host = input("Host: ")
    port = input("Port.No: ")
    database = input("Database name: ")

    return {
        'user': user,
        'password': password,
        'host': host,
        'port': port,
        'database': database
    }

# Function to create tables and insert data
def insert_data_into_db(file_path, connection):
    cursor = connection.cursor()

    # Open the file
    with open(file_path, 'r') as file:
        table_name = None
        columns = None
        for line in file:
            # If line starts with 'Data:', it's a new table
            if "Data:" in line:
                table_name = line.split()[0]
                print(f"Processing table: {table_name}")
                columns = None  # Reset columns for each table
            # Column headers come after table name
            elif table_name and columns is None:
                columns = line.strip().split(', ')
                # Create table if it doesn't exist
                create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([col + ' VARCHAR(255)' for col in columns])})"
                cursor.execute(create_table_query)
                connection.commit()
            # Data rows
            elif table_name and columns:
                values = line.strip().split(', ')

                # If values are fewer than columns, fill with None
                if len(values) < len(columns):
                    values.extend([None] * (len(columns) - len(values)))

                # If values are more than columns, trim extra values
                if len(values) > len(columns):
                    values = values[:len(columns)]

                # Insert the row into the table
                insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
                cursor.execute(insert_query, values)
                connection.commit()

    print(f"Data successfully imported into the database from {file_path}")


# Main function
def main():

    config = get_db_config()
    file_path = input("Enter the full path to the .txt file (including file name): ")


    if not os.path.exists(file_path):
        print("Error: File not found!")
        return

    try:
        connection = mysql.connector.connect(**config)
        print("Connection successful!")
        insert_data_into_db(file_path, connection)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            connection.close()

# Execute the script
if __name__ == "__main__":
    main()
