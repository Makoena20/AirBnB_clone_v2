#!/usr/bin/python3
"""
This script prepares a MySQL server for the project:

- Creates a database hbnb_test_db
- Creates a new user hbnb_test (in localhost)
- Sets the password of hbnb_test to hbnb_test_pwd
- Grants all privileges on hbnb_test_db to hbnb_test
- Grants SELECT privilege on performance_schema to hbnb_test

If the database hbnb_test_db or the user hbnb_test already exists, the script will not fail.
"""

CREATE DATABASE IF NOT EXISTS hbnb_test_db;
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

