from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Item, Category

app = Flask(__name__)

# engine for session for connection
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

# create session
Session = sessionmaker(bind=engine)
session = Session()


# homepage - displays categories and associated items
@app.route('/')
def home():
    # im not sure where this should go
    # url_for('css', filename = 'style.css')
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return render_template('index.html', cats=categories, items=items)


# create category form
@app.route('/create-category', methods=['POST', 'GET'])
def create_category():
    message = 'no data for db insert'
    if request.method == 'POST':
        cat = Category(title=request.form['title'])
        session.add(cat)
        session.commit()
        message = 'Category was inserted into db'
    return render_template("create-category.html", message=message)


# create item form
@app.route('/create-item', methods=['POST', 'GET'])
def create_item():
    message = 'no data for db insert'
    cats = query('cats')

    if request.method == 'POST':
        item = Item(title=request.form['title'],
                    description=request.form['description'],
                    category_id=request.form['category_id'])
        session.add(item)
        session.commit()
        message = 'Item was inserted into db'
    return render_template("create-item.html",
                           categories=cats,
                           message=message)


# query db for items or categories
def query(var):
    if var == 'cats':
        result = session.query(Category).all()
    elif var == 'items':
        result = session.query(Item).all()
    return result


# login
def valid_login(username, password):
    return True


# log user
def log_the_user_in(username):
    return username


# login page shows form and checks users credentials
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        # if request.method == 'POST':
        #   do_the_login()
        # else:
        # show_the_login_form()
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
