import sqlite3

def create_database(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # SQL script to create the items table
    create_table_query = """
    CREATE TABLE consumers (
    consumer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE items (
    item_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    expiry_date DATE NOT NULL
);

CREATE TABLE inventory (
    inventory_id INTEGER PRIMARY KEY,
    consumer_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (consumer_id) REFERENCES consumers (consumer_id),
    FOREIGN KEY (item_id) REFERENCES items (item_id)
);"""

    # Execute the SQL script
    cursor.execute(create_table_query)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Create the database
create_database('inventory.db')
