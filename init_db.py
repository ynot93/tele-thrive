from flask_app import db

# Drop all tables in the database
db.drop_all()
# Create all tables in the database
db.create_all()
