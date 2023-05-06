import os

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Insert 'postgres' superuser password
SUPER_USER_PASSWORD = "Yuveenhouse3090~~!!"

# Update these variables with your desired values
DB_NAME = "apps"
USER_NAME = "admin"
USER_PASSWORD = "123456789"
DB_HOST = "localhost"  # or your desired host
DB_PORT = "5432"  # or your desired port

# Connect to the PostgreSQL server using the 'postgres' superuser
conn = psycopg2.connect(f"dbname=postgres user=postgres password={SUPER_USER_PASSWORD}")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

# Create the database if it doesn't exist
cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}';")
if not cur.fetchone():
    cur.execute(f"CREATE DATABASE {DB_NAME};")
    print(f"Database '{DB_NAME}' created.")
else:
    print(f"Database '{DB_NAME}' already exists.")

# Create the user if it doesn't exist
cur.execute(f"SELECT 1 FROM pg_roles WHERE rolname='{USER_NAME}';")
if not cur.fetchone():
    cur.execute(f"CREATE USER {USER_NAME} WITH PASSWORD '{USER_PASSWORD}';")
    print(f"User '{USER_NAME}' created.")
else:
    print(f"User '{USER_NAME}' already exists.")
cur.close()
conn.close()

# Connect to the new database to grant schema privileges
conn = psycopg2.connect(f"dbname={DB_NAME} user=postgres password={SUPER_USER_PASSWORD}")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

cur.execute(f"GRANT ALL ON SCHEMA public TO {USER_NAME};")

database_url = f"postgresql://{USER_NAME}:{USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
os.environ['DATABASE_URL'] = database_url

cur.close()
conn.close()
