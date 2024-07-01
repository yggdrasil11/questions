from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS answers 
                          (id INTEGER PRIMARY KEY, question TEXT, answer INTEGER, 
                          start_time TEXT, end_time TEXT, key TEXT)''')
        conn.commit()

@app.route('/', methods=['GET, 'POST'])
def index():
    if request.method == 'POST':
        key = request.form['key']
        return redirect(url_for('questions', key=key))
    return render_template('index.html')

@app.route('/questions/<key>', methods=['GET', 'POST'])
def questions(key):
    questions = [
        "Rating of object 1", "Rating of object 2", "Test 3 points", 
        "Option of 4", "Score out of 5"
    ]
    if request.method == 'POST':
        question_index = int(request.form['question_index'])
        answer = int(request.form['answer'])
        start_time = request.form['start_time']
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO answers (question, answer, start_time, end_time, key) VALUES (?, ?, ?, ?, ?)",
                           (questions[question_index], answer, start_time, end_time, key))
            conn.commit()

        if question_index + 1 < len(questions):
            return render_template('question.html', question=questions[question_index + 1], question_index=question_index + 1, key=key, start_time=end_time)
        else:
            return "Thank you for completing the survey!"
    else:
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return render_template('question.html', question=questions[0], question_index=0, key=key, start_time=start_time)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
