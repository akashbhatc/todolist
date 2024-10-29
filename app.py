from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)

def initandconnect_db():
    connection= sqlite3.connect('todo.db')
    connection.execute('''create table if not exists todolist(id integer primary key autoincrement , task text not null)''')
    connection.commit()
    return connection

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=="POST":
        task = request.form['task']
        if task:
            with sqlite3.connect('todo.db') as connection:
                connection.execute("insert into todolist (task) values (?)", (task,))
                connection.commit()
        return redirect(url_for('index'))
    with sqlite3.connect('todo.db') as connection:
        cursor = connection.cursor()
        cursor.execute("select * from todolist")
        tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:task_id>', methods=["POST"])
def delete_task(task_id):
    with sqlite3.connect('todo.db') as connection:
        connection.execute("delete from todolist where id = ?", (task_id,))
        connection.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    initandconnect_db()
    app.run(debug=True)