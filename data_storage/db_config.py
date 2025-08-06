from peewee import SqliteDatabase
from config import DB_FILE

# ORM database instance used across the application

db = SqliteDatabase(DB_FILE)