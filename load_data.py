import pandas as pd
import psycopg2

# Connection settings for the local Postgres container defined in docker-compose.yml
DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "campus_bites",
    "user": "postgres",
    "password": "postgres",
}

# Path to the source CSV file
CSV_PATH = "data/campus_bites_orders.csv"

# SQL statement to create the orders table if it doesn't already exist.
# Running this multiple times is safe — it won't overwrite existing data.
CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    order_id           INTEGER PRIMARY KEY,
    order_date         DATE,
    order_time         TIME,
    customer_segment   VARCHAR(50),
    order_value        NUMERIC(10, 2),
    cuisine_type       VARCHAR(50),
    delivery_time_mins INTEGER,
    promo_code_used    VARCHAR(3),
    is_reorder         VARCHAR(3)
);
"""

def load():
    # Read the CSV into a DataFrame
    df = pd.read_csv(CSV_PATH)
    print(f"Read {len(df)} rows from {CSV_PATH}")

    # Open a connection to the database and create a cursor to execute SQL
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    # Create the orders table if it doesn't exist yet
    cur.execute(CREATE_TABLE)

    # Convert the DataFrame to a list of plain tuples, one per row.
    # executemany expects an iterable of tuples matching the INSERT column order.
    rows = list(df.itertuples(index=False, name=None))
    cur.executemany(
        """
        INSERT INTO orders
            (order_id, order_date, order_time, customer_segment, order_value,
             cuisine_type, delivery_time_mins, promo_code_used, is_reorder)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        rows,
    )

    # Commit the transaction so the data is persisted, then close the connection
    conn.commit()
    cur.close()
    conn.close()
    print(f"Loaded {len(rows)} rows into orders table")

# Only run load() when this script is executed directly,
# not when it's imported as a module by another script
if __name__ == "__main__":
    load()
