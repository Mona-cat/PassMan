import sqlite3
import mysql.connector

# x = 123456
# y = "Hallo"
# z = "test"

# test = [(111111, "Test", "Test"),
#         (111112, "Test", "Test"),
#         (111113, "Test", "Test")]


connection = sqlite3.connect("database.db")

cursor = connection.cursor() #Verbindung mit DB um commands auszuführen

sql_create = "CREATE TABLE Students (id INT PRIMARY KEY, fname VARCHAR(20), lname VARCHAR(20))"

sql_insert = "INSERT INTO Students VALUES(?, ?, ?)"

sql_select = "SELECT * FROM Students "

if(not cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='table_name';")):
    cursor.execute(sql_create)


# cursor.executemany(sql_insert, test)

res = cursor.execute(sql_select)

for row in res:
    print(row)

connection.commit()
connection.close()

