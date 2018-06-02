##Catalog App. - FSD Project 3
This application uses CRUD to display, create, update, and delete catalog categories and associated items.

GitHub OAuth2 is used to authenticate users to store a session variable: <code>/login</code>

A JSON endpoint is available for catalog/item data at: <code>/catalog.json</code>

###The Repo. Contains the Following Files
 1. application.py - Contains routing and functionality.
 2. database_setup.py - Contains database class to generate catalog.db - Will overwrite catalog.db with a blank version if db exists prior to running the script.
 3. catalog.db - Database for project.
 4. Files in templates directory - Contains Jinja2 page templates.
 5. static/css/style.less - Contains Less CSS for template styling.
 6. README.md

###How to Run the Application
Python 2.7, PostgreSQL, requests_oathlib, and Flask-Login must be installed and configured.

Creating a GitHub account and an app. is necessary to obtain and replace the <code>client_id</code> and <code>client_secret</code> variables at the top of the application.py file.

GitHub app. Homepage URL: <code>http://localhost:8000</code> 

Authorization Callback URL: <code>http://localhost:8000/callback</code>

In the terminal, clone the repo., then navigate to the directory where the files are located.

The catalog database can be built by running the database_setup.py file if the existing database (catalog.db) does not already exist.

Running application.py will start the server, then you will be able to visit the website at:
<code>http://localhost:8000</code>

After clicking the Login link, you will be required to authenticate through GitHub. This will allow you to create, edit, and delete Categories and Items.
<pre>
    <code>$ pip install requests requests_oauthlib</code>
    <code>$ pip install Flask-Login</code>
	<code>$ git clone https://github.com/mikelewek/FSD_P3_ItemCatalog.git</code>
	<code>$ cd FSD_P3_ItemCatalog</code>
	<code>$ python database_setup.py</code>
	<code>$ python application.py</code>
</pre>


Requests-OAuthlib used for GitHub OAuth: [Requests-OAuthlib] (http://requests-oauthlib.readthedocs.org/en/latest/index.html)

If the user is not authorized and attempts to visit a restricted page (create, update, or delete categories or items), the user will be redirected back to the homepage.