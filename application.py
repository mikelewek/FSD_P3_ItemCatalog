
from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine
from database_setup import Base, Item, Category

app = Flask(__name__)

# Homepage - displays categories and associated items
@app.route('/')
def homePage():
    #categories = session.query(Category).all()
    #items = session.query(Item).all()
    return render_template('index.html')


if __name__ == '__main__':
        app.run(host = '0.0.0.0', port = 8000, debug = True)