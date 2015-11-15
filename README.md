Catalog App. - FSD Project 3
------------------------------------
<p>This application uses CRUD to display, create, update, and delete catalog categories and their associated items.</p>
<p>Google OAuth is used to authenticate users: /login</p>
<p>A JSON endpoint is available for catalog/item data at: /catalog.json</p>

The Repo. Contains the Following Files
-------------------------------------
 1. application.py - Contains routing and functionality.<br>
 2. database_setup.py - Contains database class. Generates catalog.db - Will overwrite catalog.db with a blank version if db exists prior to running the script.<br>
 3. catalog.db - Database for project.<br>
 4. Files in templates directory - Contains Jinja1 page templates.<br>
 5. static/css/style.less - Contains Less CSS for template styling.<br>
 6. README.md

<br>
<p>Requests-OAuthlib used for OAuth: <a href="http://requests-oauthlib.readthedocs.org/en/latest/index.html" target="_blank">Requests-OAuthlib</a></p>