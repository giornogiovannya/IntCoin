from flask import Flask, render_template
import sqlite3
import db
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/goods')
def goods():
    goodsList = db.selectAll()
    return goodsList

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

