# flask-website
website to sign up ,create,edit, delte post , view every one post 

Flask Blog Application – Image Upload, Authentication & CRUD

Overview

This is a simple Flask web application for blogging. It allows users to register and log in securely, create posts with images, edit and delete their own posts, and view a homepage with all blog entries.

Main Features

* User registration with password hashing
* Secure login/logout using session
* Create posts with optional image upload
* Edit and replace images for existing posts
* Delete posts (only your own)
* Display images in blog list and detail pages
* Flash messages for user feedback
* Clean Bootstrap 5 styling
* Route protection: only logged-in users can post/edit/delete

Requirements

* Python 3.x
* PostgreSQL
* pip
* virtualenv (recommended)
* Flask and dependencies

Project Structure

flask-blog/
│
├── app.py                 # Main Flask app
├── db\_config.py           # PostgreSQL connection function
├── create\_tables.sql      # SQL script to create users and posts tables
├── static/
│   └── pics/              # Folder to store uploaded images
│
├── templates/             # HTML templates using Bootstrap
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── create\_post.html
│   ├── edit\_post.html
│
└── README.md              # This file

Setup Instructions for Linux and Windows

1. Clone the Repository

git clone [https://github.com/yourusername/flask-blog.git](https://github.com/yourusername/flask-blog.git)
cd flask-blog

2. Create a Virtual Environment

Linux/macOS:

python3 -m venv venv
source venv/bin/activate

Windows:

python -m venv venv
venv\Scripts\activate

3. Install Required Packages

pip install flask psycopg2-binary werkzeug

You can also create a requirements.txt using:

pip freeze > requirements.txt

4. PostgreSQL Setup

a. Open PostgreSQL:

psql -U postgres

Then run:

CREATE DATABASE flask;
CREATE USER flaskuser WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE flask TO flaskuser;

b. Run the SQL file to create tables:

psql -U flaskuser -d flask -f create\_tables.sql

This creates:

* users table: id, username, password
* posts table: id, title, content, image (file path), owner (foreign key)

5. Configure db\_config.py

Create a file named db\_config.py:

import psycopg2

def get\_db\_connection():
return psycopg2.connect(
dbname='flask',
user='flaskuser',
password='yourpassword',
host='localhost'
)

6. Run the Application

python app.py

By default, it will be available at:
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

How to Use the App

1. Register

Go to /register
Fill in username, password, and confirm password
You will see flash messages for success or error

2. Login

Go to /login
Enter valid credentials
If correct, you will be redirected to the home page

3. Create a Post

Go to /create
Enter a title, content, and optionally upload an image
Image will be saved in static/pics
The post is linked to the logged-in user

4. Edit or Delete Posts

Only your posts will show Edit and Delete buttons
Edit allows updating the post and replacing the image
Delete removes the post and deletes the image

5. Logout

Go to /logout
Your session will be cleared and you will return to the homepage

Image Upload Notes

* Allowed image types: .jpg, .jpeg, .png, .gif
* Filenames are secured using werkzeug's secure\_filename
* Images are saved in static/pics
* When editing, the old image is deleted if replaced
* Images are displayed in the home page and post view

Security and Validation

* Passwords are hashed using Werkzeug (generate\_password\_hash)
* Session is used for login state
* Route protection: users cannot access create/edit/delete unless logged in
* Uploads are validated for allowed image types
* Flash messages are shown for feedback (errors, success, warnings)

Extra Notes

* Styled using Bootstrap 5
* Navigation bar with links to login, logout, register, and create post
* Responsive layout and user-friendly design

Screenshots to Submit (for lab report)

* Home page showing posts with images
* A new post with uploaded image
* Edited post with a new image
* Showing Edit/Delete buttons only on your own posts

Running on a Different Port

To run on port 8000:

python app.py --port 8000

To enable debug mode:

app.run(debug=True)



