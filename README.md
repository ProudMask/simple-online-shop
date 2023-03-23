# Simple Online Shop
This is a simple web application that allows users to create accounts, log in, and view a list of products. It is built using Flask and SQLite.

## Installation
To install the application, follow these steps:

1. Install requirements
   ```
   pip install -r requirements.txt 
   ```
   
2. Set up the database:
   ```
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```
3. Set up the flask environment
   ```
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export FLASK_SECRET_KEY=<your_secret_key_here>
   ```
4. start the server
   ```
   flask run
   ```
 
 The application should now be accessible at http://localhost:5000.
 
