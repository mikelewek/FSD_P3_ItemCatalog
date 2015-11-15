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
    # get all category and items
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return render_template('index.html',
                           cats=categories,
                           items=items)


# catalog JSON endpoint
@app.route('/catalog.json', methods=['POST', 'GET'])
def catalog_json():
    json = ''
    return render_template("create-category.html", json=json)


# create category
@app.route('/catalog/category/create', methods=['POST', 'GET'])
def create_category():
    message = 'No data for db insert'

    if request.method == 'POST':
        cat = Category(title=request.form['title'])
        session.add(cat)
        session.commit()
        message = 'Category was inserted into db'
    return render_template("create-category.html", message=message)


# edit category
@app.route('/catalog/category/<title>/edit', methods=['POST', 'GET'])
def edit_category(title):
    message = ''
    # get item by query string title
    cat = session.query(Category).filter_by(title=title)

    # update item in db when form is submitted
    if request.method == 'POST':
        title = request.form['title']
        cat = Category(title=title)
        session.add(cat)
        session.commit()
        message = 'Category updated successfully'
    return render_template("edit-category.html",
                           title=title,
                           cat=cat,
                           message=message)


# delete category
@app.route('/catalog/<title>/delete', methods=['POST', 'GET'])
def delete_category(title):
    message = 'Warning! Pressing Submit will permanently delete the catogory!'

    if request.method == 'POST':
        message = ''
    return render_template("delete-category.html",
                           title=title,
                           message=message)


# display category items
@app.route('/catalog/category/<title>/items', methods=['POST', 'GET'])
def show_items(title):
    items = session.query(Category.id, Item.title, Item.description).\
                join(Item).\
                filter(Category.title == title)
    return render_template("show-category.html",
                           items=items)


# create item
@app.route('/catalog/<title>/create', methods=['POST', 'GET'])
def create_item(title):
    message = 'No data for db insert'
    cats = session.query(Category).all()

    if request.method == 'POST':
        item = Item(title=request.form['title'],
                    description=request.form['description'],
                    category_id=request.form['category_id'])
        session.add(item)
        session.commit()
        message = 'Item was inserted into db'
    return render_template("create-item.html",
                           title=title,
                           categories=cats,
                           message=message)


# edit item
@app.route('/catalog/<qid>/edit', methods=['POST', 'GET'])
def edit_item(qid):
    cats = session.query(Category).all()
    items = session.query(Item).filter_by(id=qid)
    message = ''

    if request.method == 'POST':
        session.query(Item).\
            filter(Item.id == request.form['id']).\
            update({'title': request.form['title'],
                    'description': request.form['description'],
                    'category_id': request.form['category_id']})
        message = 'Item successfully updated'
    return render_template("edit-item.html",
                           items=items,
                           categories=cats,
                           message=message)


# delete item
@app.route('/catalog/<category>/<title>/delete', methods=['POST', 'GET'])
def delete_item(title):
    message = 'Warning! Pressing Submit will permanently delete the catogory!'

    if request.method == 'POST':
        message = ''
    return render_template("delete-item.html",
                           title=title,
                           message=message)


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
