from flask import Flask, render_template, g, request, redirect   # This imports flask and the other things that this program needs
import sqlite3 

app = Flask(__name__)

DATABASE = 'mini.db'  

def get_db():   # This connects the database to my website
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):    # this closes the database is the website is closed
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/index', methods=['GET', 'POST'])
def index():    # this gets information from another file and brings it up
    return render_template('index.html')   # it tells the computer what the file is called that it needs to bring up

@app.route('/')
def home():    # this gets information from the home page file and brings it up
    cursor = get_db().cursor()     # this gets the database to be connected to the website
    sql = "SELECT * FROM shopping_cart"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('home.html', results = results)    # it tells the computer what the file is called that it needs to bring up

@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        cursor = get_db().cursor()     # this gets the database to be connected to the website
        new_name = request.form["item"]
        new_cost = request.form["cost"]
        sql = "INSERT INTO shopping_cart(item,cost) VALUES (?,?)"
        cursor.execute(sql,(new_name, new_cost))
        get_db().commit()
    return redirect('/')

@app.route('/example', methods=['GET', 'POST'])
def example():    # this is an example page I made and kept on here as a little secret for people to find if they wish to do so
    links = ['https://www.youtube.com']    # this is a string of websites that the user can press on and go to
    return render_template('example.html', links=links)    # it tells the computer what the file is called that it needs to bring up

if __name__ == '__main__':    # this runs the application
    app.run(debug=True)