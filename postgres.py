import psycopg2

conn = psycopg2.connect(
  database="price_mining",
  host="localhost",
  user="a1398user",
  password="tuyen123",
  port="5432"
)

print(conn)