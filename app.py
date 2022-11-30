import os.path
import sys

from flask import  ( Flask, g , redirect, render_template, request, session, url_for )
    

from lib.tablemodel import DatabaseModel
from lib.demodatabase import create_demo_database


# a simple demo dataset will be created.
LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True


class User:
    def __init__(self, id, username, password):

        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Kenan', password='KenanWW'))
users.append(User(id=2, username='Ruben', password='RubenWW'))
users.append(User(id=3, username='Maarten', password='MaartenWW'))
users.append(User(id=4, username='Aisha', password='AishaWW'))

app = Flask(__name__)
app.secret_key = 'geheimekey'

@app.before_request
def before_request():
    g.user = None


    if 'user_id' in session:
            user = [x for x in users if x.id == session['user_id']][0]
            g.user = user


@app.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        session.pop('user_id', None)
        
        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('index'))
    
        return redirect(url_for('login'))

    return render_template('login.html')



@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')




# This command creates the "<application directory>/databases/testcorrect_vragen.db" path
DATABASE_FILE = os.path.join(app.root_path, 'databases', 'testcorrect_vragen.db')

# Check if the database file exists. If not, create a demo database
if not os.path.isfile(DATABASE_FILE):
    print(f"Could not find database {DATABASE_FILE}, creating a demo database.")
    create_demo_database(DATABASE_FILE)
dbm = DatabaseModel(DATABASE_FILE)

# Main route that shows a list of tables in the database
# Note the "@app.route" decorator. This might be a new concept for you.
# It is a way to "decorate" a function with additional functionality. You
# can safely ignore this for now - or look into it as it is a really powerful
# concept in Python.
@app.route("/")
def index():
    if not g.user:
        return redirect(url_for('login'))
    tables = dbm.get_table_list()
    return render_template(
        "tables.html", table_list=tables, database_file=DATABASE_FILE
    )
    


# The table route displays the content of a table
@app.route("/table_details/<table_name>")
def table_content(table_name=None):
    if not g.user:
        return redirect(url_for('login'))
    if not table_name:
        return "Missing table name", 400  # HTTP 400 = Bad Request
    else:
        rows, column_names = dbm.get_table_content(table_name)
        return render_template(
            "table_details.html", rows=rows, columns=column_names, table_name=table_name
        )


if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)
