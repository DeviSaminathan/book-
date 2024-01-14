
from flask import Flask,render_template,url_for,redirect,request, url_for, session
import model
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'humancomputerinterfacelab'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Asguard@17'
app.config['MYSQL_DB'] = 'book'
 
mysql = MySQL(app)

book_title_list=model.book_title_list

@app.route('/',methods = ['POST','GET'])
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('home.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('main.html', msg = msg)


@app.route('/lp',methods = ['POST','GET'])
def lp():
    return render_template("login.html")


@app.route('/home',methods = ['POST','GET'])
def home():
    return render_template("home.html")



@app.route('/sp',methods = ['POST','GET'])
def sp():
    return render_template("register.html")


@app.route('/knn1',methods = ['POST','GET'])
def knn1():
    if request.method == 'POST':
        selected_book = request.form['book-name-knn']
        return redirect(url_for('knn',knn= selected_book ))

    else:
        return render_template("knn1.html",book_list =book_title_list)

@app.route('/svd',methods = ['POST','GET'])
def svd():
    if request.method == 'POST':
        selected_book = request.form['book-name']
        return redirect(url_for('book',book= selected_book ))

    else:
        return render_template("svd.html",book_list =book_title_list)


@app.route('/<book>')
def book(book):
    final_list=model.bookRecommendation(book)
    url_list=model.imgUrlList(final_list)
    return render_template('book.html',final_list=final_list,book_selected=book,url_list=url_list)

@app.route('/<knn>_test')
def knn(knn):
    final_book_list=model.methodTwo(knn)
    url_list=model.imgUrlList(final_book_list)
    return render_template('knn.html',final_book_list=final_book_list,book_selected=knn,url_list=url_list)

 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
 
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO login VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('home.html', msg = msg)


if __name__ == "__main__":
    app.run(debug=False)