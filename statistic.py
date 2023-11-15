from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', no_data=False)

@app.route('/statistic', methods=['POST'])
def statistic():

    conn = sqlite3.connect('statistic.db')
    cursor = conn.cursor()

    cursor.execute("SELECT player_name,score,level, mode FROM statistic")
    statistic_data = cursor.fetchall()

    conn.close()

    if not statistic_data:
        return render_template('index.html', no_data=True)
    
    return render_template('index.html', statistic_data=statistic_data)
