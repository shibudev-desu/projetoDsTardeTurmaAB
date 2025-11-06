from peewee import PostgresqlDatabase

db = PostgresqlDatabase(
    "postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port=2222
)
