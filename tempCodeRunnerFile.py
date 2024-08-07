from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import update

# Specify the path to your SQLite database file
DATABASE_URL = 'sqlite:///C:/Users/A/OneDrive/Desktop/SkyGram/users.db'

# Create an engine and connect to the database
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Reflect the database schema
metadata = MetaData()
metadata.reflect(bind=engine)

# Specify the table name and column names
table_name = 'users'  # Replace with your actual table name
table = Table(table_name, metadata, autoload_with=engine)

# Define the update statement
stmt_update = update(table).where(
    table.c.email == 'ashish2002@gmail.com'
).values(email='info@skygramstays.in')

# Execute the update statement
with engine.connect() as connection:
    result = connection.execute(stmt_update)
    print(f"Number of rows updated: {result.rowcount}")

    # Define and execute the select statement to display table contents
    stmt_select = table.select()
    result = connection.execute(stmt_select)
    
    # Print the table contents
    print("\nTable Contents:")
    for row in result:
        print(row)

# Commit the transaction
session.commit()

# Close the session
session.close()
