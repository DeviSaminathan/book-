from mysql import connector

def dbconnect(x):
    mydb = connector.connect(
        host="localhost",
        user="root",
        password="Asguard@17",
        database="book"
    )
    mycursor = mydb.cursor()
    if x == 1 :
        mycursor.execute("SELECT * FROM bx-books")
        books = mycursor.fetchall()
        return books
    if x == 2 :
        mycursor.execute("SELECT * FROM bx-users")
        users = mycursor.fetchall()
        return ratings
    if x == 3 :
        mycursor.execute("SELECT * FROM bx-book-ratings")
        ratings = mycursor.fetchall()
        return users
    mydb.close()