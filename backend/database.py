import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def get_schema() -> str:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]

    schema = ""
    for table in tables:
        cursor.execute(f"DESCRIBE {table}")
        columns = cursor.fetchall()
        col_definitions = ", ".join(
            f"{col[0]} ({col[1]})" for col in columns
        )
        schema += f"Table: {table}\nColumns: {col_definitions}\n\n"

    cursor.close()
    conn.close()
    return schema.strip()

def run_query(sql: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql)

    sql_type = sql.strip().split()[0].upper()

    if sql_type == "SELECT":
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"type": "select", "columns": columns, "rows": rows}
    else:
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        return {"type": "modify", "affected_rows": affected}

def seed_database():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = conn.cursor()

    cursor.execute("DROP DATABASE IF EXISTS ecommerce_db")
    cursor.execute("CREATE DATABASE ecommerce_db")
    cursor.execute("USE ecommerce_db")

    cursor.execute("""
        CREATE TABLE customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            city VARCHAR(50),
            joined_date DATE
        )
    """)

    cursor.execute("""
        CREATE TABLE products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            category VARCHAR(50),
            price DECIMAL(10, 2),
            stock INT
        )
    """)

    cursor.execute("""
        CREATE TABLE orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            product_id INT,
            quantity INT,
            order_date DATE,
            total_amount DECIMAL(10, 2),
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    cursor.executemany(
        "INSERT INTO customers (name, email, city, joined_date) VALUES (%s, %s, %s, %s)",
        [
            ("Amit Sharma", "amit@gmail.com",  "Mumbai",    "2023-01-15"),
            ("Priya Patel", "priya@gmail.com", "Delhi",     "2023-03-22"),
            ("Rahul Verma", "rahul@gmail.com", "Bengaluru", "2023-05-10"),
            ("Sneha Iyer",  "sneha@gmail.com", "Chennai",   "2023-07-08"),
            ("Karan Mehta", "karan@gmail.com", "Pune",      "2023-09-30"),
        ]
    )

    cursor.executemany(
        "INSERT INTO products (name, category, price, stock) VALUES (%s, %s, %s, %s)",
        [
            ("Laptop",     "Electronics", 55000.00, 30),
            ("Smartphone", "Electronics", 25000.00, 80),
            ("Desk Chair", "Furniture",    8000.00, 50),
            ("Headphones", "Electronics",  3500.00, 120),
            ("Bookshelf",  "Furniture",    5000.00, 40),
            ("Keyboard",   "Electronics",  2000.00, 150),
        ]
    )

    cursor.executemany(
        "INSERT INTO orders (customer_id, product_id, quantity, order_date, total_amount) VALUES (%s, %s, %s, %s, %s)",
        [
            (1, 1, 1, "2024-01-10", 55000.00),
            (2, 2, 2, "2024-01-15", 50000.00),
            (3, 4, 1, "2024-02-05",  3500.00),
            (4, 3, 3, "2024-02-20",  8000.00),
            (1, 6, 2, "2024-03-01",  4000.00),
            (5, 1, 1, "2024-03-15", 55000.00),
            (2, 5, 2, "2024-04-10", 10000.00),
            (3, 2, 1, "2024-04-22", 25000.00),
        ]
    )

    conn.commit()
    cursor.close()
    conn.close()
    print("Database seeded fresh successfully!")
