import subprocess
import os   
import pymysql
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


# database configuration changes based on environment variables
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'database': os.getenv('DB_NAME', 'mydatabase')
}

def get_user_input():
    user_input = input('Enter your name: ')
    return user_input

def send_email(to, subject, body):
    try:
        # os.system() is replaced with subprocess.run() for better security and error handling
        subprocess.run(
            ['sendmail', to],
            input=body,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        # exception handling for subprocess errors
        print(f"Failed to send email: {e}")

def get_data():
    # using a secure API endpoint and handling potential errors
    url = 'https://secure-api.com/get-data'
    try:
        response = urlopen(url)
        data = response.read().decode()
        return data
    except (URLError, HTTPError) as e:
        print(f"Failed to fetch data: {e}")
        return None
    

def save_to_db(data):
    if data is None:
        print("No data to save to the database.")
        return
    
    # string formatting is replaced with parameterized queries to prevent SQL injection
    query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(query, (data, "Another Value"))
        connection.commit()
        
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
