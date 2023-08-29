import sqlite3

connection = sqlite3.connect('notes.db')
c = connection.cursor()


with open('schema.sql') as f:
    c.executescript(f.read())


connection.commit()
connection.close()