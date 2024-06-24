from app import db, Villa

# Drop the villa table
db.drop_all()
# Create the villa table without the unique constraint
db.create_all()
