from requests_oauthlib import OAuth2Session
from flask import Flask, flash, render_template, request, \
    redirect, session, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Item, Category
import os

app = Flask(__name__)

# engine for session for connection
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

# create session
Session = sessionmaker(bind=engine)
dbSession = Session()


# This information is obtained upon registration of a new GitHub OAuth
# application here: https://github.com/settings/applications/new
client_id = 'xx'
client_secret = 'xx'
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'


@app.route("/login")
def login():
    """ User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.
@app.route("/callback", methods=["GET"])
def callback():
    """ Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    session['oauth_token'] = token
    return redirect(url_for('home', message="You have successfully logged in."))


# check if user is authenticated
def is_auth():
    authenticated = False
    try:
        if session['oauth_token']:
            authenticated = True
    except KeyError:
        authenticated = False
    return authenticated


# homepage displays categories and associated items
@app.route('/', methods=['POST', 'GET'])
def home():
    auth = is_auth()
    message = ''
    categories = ''
    items = ''

    if request.method == 'GET':
        message = request.args.get('message')

    # get all category and items
    # or display no results found
    categories = dbSession.query(Category).all()
    if len(categories) == 0:
        categories = [{'title': 'No Categories found.'}]
    items = dbSession.query(Category).all()
    if len(items) == 0:
        items = [{'title': 'No Items found.'}]

    return render_template('index.html',
                           cats=categories,
                           items=items,
                           message=message,
                           loggedIn=auth)


# catalog JSON endpoint
@app.route('/catalog.json')
def catalog_json():
    list = []
    items = dbSession.query(Item).all()
    for item in items:
        list.append({'id': item.id,
                     'category_id': item.category.id,
                     'category_title': item.category.title,
                     'title': item.title,
                     'description': item.description,
                     })
    return jsonify({"items": list})


@app.route('/catalog/category/create', methods=['POST', 'GET'])
def create_category():
    """ create category

    Check if user is logged in and show form. If user is not
    logged in, redirect to home and display message. When
    data is submitted, add object to database.
    """
    auth = is_auth()
    message = ''
    if is_auth() is not True:
        return redirect(url_for('home', message="You must be logged-in to that page!"))

    if request.method == 'POST' and is_auth() == True:
        cat = Category(title=request.form['title'])
        dbSession.add(cat)
        dbSession.commit()
        message = 'Category was inserted into db'
    return render_template("create-category.html",
                           message=message,
                           loggedIn=auth)


# edit category
@app.route('/catalog/category/<qid>/edit', methods=['POST', 'GET'])
def edit_category(qid):
    message = ''
    # get item by query string id
    cat = dbSession.query(Category).filter_by(id=qid)

    # update item in db when form is submitted
    if request.method == 'POST':
        title = request.form['title']
        cat = Category(id=qid)
        dbSession.add(cat)
        dbSession.commit()
        message = 'Category updated successfully'
    return render_template("edit-category.html",
                           title=title,
                           cat=cat,
                           message=message)


# delete category
@app.route('/catalog/<int:qid>/delete', methods=['POST', 'GET'])
def delete_category(qid):
    message = 'Warning! Pressing Submit will permanently delete the category!'

    if request.method == 'POST':
        message = ''
    return render_template("delete-category.html",
                           id=qid,
                           message=message)


# display category with items
@app.route('/catalog/category/<int:qid>/items', methods=['POST', 'GET'])
def show_items(qid):
    items = dbSession.query(Category.title.label('cat_title'), Category.id, Item.title.label('item_title'),
                            Item.description).join(Item).filter(Category.id == qid)
    return render_template("show-category.html",
                           items=items)


# display individual item
@app.route('/catalog/item/<int:qid>', methods=['POST', 'GET'])
def show_item(qid):
    auth = is_auth()
    item = dbSession.query(Item.id, Item.title, Item.description).filter_by(id=qid)
    return render_template("show-item.html",
                           item=item,
                           loggedIn=auth)


# create item
@app.route('/catalog/item/create', methods=['POST', 'GET'])
def create_item():
    """ create item

    Check if user is logged in and show form. If user is not
    logged in, redirect to home and display message. When
    data is submitted, add object to database.
    """
    auth = is_auth()
    message = ''
    if is_auth() is not True:
        return redirect(url_for('home', message="You must be logged-in to that page!"))
    cats = dbSession.query(Category).all()

    # display message if no categories have been created to
    # populate the item select dropdown
    if len(cats) == 0:
        cats = 0
        message = 'No Categories found. Creating a Category is ' \
                  'required prior to creating a new item!'

    if request.method == 'POST':
        item = Item(title=request.form['title'],
                    description=request.form['description'],
                    category_id=request.form['category_id'])
        dbSession.add(item)
        dbSession.commit()
        message = 'Item was inserted into db'
    return render_template("create-item.html",
                           categories=cats,
                           message=message,
                           loggedIn=auth)


# edit item
@app.route('/catalog/item/<int:qid>/edit', methods=['POST', 'GET'])
def edit_item(qid):
    auth = is_auth()
    if is_auth() is not True:
        return redirect(url_for('home', message="You must be logged-in to that page!"))
    cats = dbSession.query(Category).all()
    items = dbSession.query(Item).filter_by(id=qid)
    message = ''

    if request.method == 'POST':
        dbSession.query(Item).\
            filter(Item.id == request.form['id']).\
            update({'title': request.form['title'],
                    'description': request.form['description'],
                    'category_id': request.form['category_id']})
        message = 'Item successfully updated'
    return render_template("edit-item.html",
                           items=items,
                           categories=cats,
                           message=message,
                           loggedIn=auth)


# delete item
@app.route('/catalog/item/<int:qid>/delete', methods=['POST', 'GET'])
def delete_item(qid):
    auth = is_auth()
    if is_auth() is not True:
        return redirect(url_for('home', message="You must be logged-in to that page!"))
    message = 'Warning! Pressing Submit will permanently delete the item!'
    item = dbSession.query(Item.id, Item.title).filter_by(id=qid)
    if request.method == 'POST':
        message = ''
    return render_template("delete-item.html",
                           item=item,
                           message=message,
                           loggedIn=auth)


if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0', port=8000, debug=True)
