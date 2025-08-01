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

if __name__ == '__main__':
    app.run(debug=True)
