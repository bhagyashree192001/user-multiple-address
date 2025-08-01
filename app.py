<<<<<<< HEAD
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",  # add your password
    database="virtual_office"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    tasks = cursor.fetchall()
    return render_template('dashboard.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form['task']
    if task:
        cursor.execute("INSERT INTO tasks (task) VALUES (%s)", (task,))
        db.commit()
    return redirect('/')
=======
from flask import Flask, render_template, redirect, url_for, request, session
from flask_mysqldb import MySQL
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    (username, email, password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], password_input):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, address FROM addresses WHERE user_id = %s", (session['user_id'],))
    addresses = cur.fetchall()

    if request.method == 'POST':
        address = request.form['address']
        cur.execute("INSERT INTO addresses (user_id, address) VALUES (%s, %s)",
                    (session['user_id'], address))
        mysql.connection.commit()

    cur.close()
    return render_template('dashboard.html', addresses=addresses, username=session['username'])

@app.route('/delete_address/<int:address_id>')
def delete_address(address_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM addresses WHERE id = %s AND user_id = %s",
                (address_id, session['user_id']))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
>>>>>>> 38fa9874513c9896b364a4da9bc5be1fed48d4c4

if __name__ == '__main__':
    app.run(debug=True)
