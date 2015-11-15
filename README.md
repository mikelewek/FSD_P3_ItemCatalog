Catalog App. - FSD Project 3
---------------------------
<p>This application uses CRUD to display, create, update, and delete catalog categories and associated items.</p>
<p>Google OAuth is used to authenticate users: <code>/login</code></p>
<p>A JSON endpoint is available for catalog/item data at: <code>/catalog.json</code></p>

The Repo. Contains the Following Files
-------------------------------------
 1. application.py - Contains routing and functionality.<br>
 2. database_setup.py - Contains database class to generate catalog.db - Will overwrite catalog.db with a blank version if db exists prior to running the script.<br>
 3. catalog.db - Database for project.<br>
 4. Files in templates directory - Contains Jinja2 page templates.<br>
 5. static/css/style.less - Contains Less CSS for template styling.<br>
 6. README.md

How to Run the Application
-------------------------
<p>Python 2.7, PostgreSQL, and requests_oathlib must be installed and configured.</p>
<p>In the terminal, clone the repo., then navigate to the directory where the files are located.</p>
<p>The catalog database can be re-built by running the database_setup.py file, otherwise existing data will be consumed from catalog.db</p>
<p>Running application.py will start the server, then you will be able to visit the website at <code>http:localhost:8000</code></p>

<pre>
    <code>$ pip install requests requests_oauthlib</code>
	<code>$ git clone https://github.com/mikelewek/FSD_P3_ItemCatalog.git</code>
	<code>$ cd FSD_P3_ItemCatalog</code>
	<code>$ python application.py</code>
</pre>

<br>
<p>Requests-OAuthlib used for Google OAuth: <a href="http://requests-oauthlib.readthedocs.org/en/latest/index.html" target="_blank">Requests-OAuthlib</a></p>