from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Item, Category
import pprint

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
    categories = query('cats', False)
    items = query('items', False)
    return render_template('index.html',
                           cats=categories,
                           items=items)


# create category
@app.route('/create-category', methods=['POST', 'GET'])
def create_category():
    message = 'No data for db insert'

    if request.method == 'POST':
        cat = Category(title=request.form['title'])
        session.add(cat)
        session.commit()
        message = 'Category was inserted into db'
    return render_template("create-category.html", message=message)


# edit category
@app.route('/edit-category/<int:id>', methods=['POST', 'GET'])
def edit_category(id):
    message = ''
    cat = query('cats', id)

    if request.method == 'POST':
        cat = Category(title=request.form['title'])
        session.add(cat)
        session.commit()
        message = 'Category updated successfully'
    return render_template("edit-category.html",
                           cat=cat,
                           message=message)


# delete item
@app.route('/delete-category/<int:id>', methods=['POST', 'GET'])
def delete_category(id):
    delete = query('cats', id, True)
    return render_template("edit-category.html",
                           message=delete)


# create item
@app.route('/create-item', methods=['POST', 'GET'])
def create_item():
    message = 'No data for db insert'
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


# edit item
@app.route('/edit-item/<int:id>', methods=['POST', 'GET'])
def edit_item(id):
    cats = query('cats')
    items = query('items', id)
    message = ''

    if request.method == 'POST':
        item = Item(title=request.form['title'],
                    description=request.form['description'],
                    category_id=request.form['category_id'])
        session.add(item)
        session.commit()
        message = 'Item successfully updated'
    return render_template("edit-item.html",
                           items=items,
                           categories=cats,
                           message=message)


# delete item
@app.route('/delete-item/<int:id>', methods=['POST', 'GET'])
def delete_item(id):
    delete = query('items', id, True)
    return render_template("edit-item.html",
                           message=delete)



# query db for items or categories
def query(table, qid=False, delete=False):
    result = ''

    # category db queries
    if table == 'cats':
        if delete is not False:
            #delete query here
            result = 'cat ' + qid + ' deleted successfully'
        elif qid is not False:
            result = session.query(Category).filter_by(id=qid)
        else:
            result = session.query(Category).all()

    # items db queries
    if table == 'items':
        if delete is not False:
            #delete query here
            result = 'item ' + qid + ' deleted successfully'
        elif qid is not False:
            result = session.query(Item).filter_by(id=qid)
        else:
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
