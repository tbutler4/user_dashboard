from flask import Flask, session, flash, render_template, request, redirect
import re
import pymysql.cursors
from flask_bcrypt import Bcrypt  
from mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
passwordRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')
app = Flask(__name__)
app.secret_key = 'hidden'
bcrypt = Bcrypt(app)
mysql = connectToMySQL("projectdb")

@app.route('/')
def index():
    return render_template("userdash.html")

@app.route('/begin', methods=['POST'])
def begin():
    return render_template("login.html")

@app.route('/reg')
def reg():
    return render_template('register.html')

@app.route('/log')
def log():
    return render_template('login.html')

@app.route('/success', methods=["post"])
def success():
    good_form = True

    print (request.form['email'])
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!")
        good_form = False

    print (request.form['email'])
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
        good_form = False

    #get email and password from the database and compare it to user input
    query = 'SELECT * from users where email = %(email)s;'
    # 
    data = {
        'email':request.form['email']
        }
    logged = mysql.query_db(query,data)
    print(logged)

    if logged == ():
        flash("User email does not exist")
        good_form = False

    elif request.form['pword'] != logged[0]['pword']:
        flash("password does not work")
        good_form = False

    if good_form == False:
                return redirect("/log")

    return render_template('dash.html')


@app.route('/off')
def off():
    return render_template('login.html')

@app.route('/dashdash', methods=["POST"])
def dashdash():
    good_form = True
    rod = request.form['email']
    pope = request.form['first_name']
    tom = request.form['last_name']
    clance = request.form['pword']

    print (request.form['email'])
    if len(request.form["email"]) < 1:
        flash('email cannot be blank')
        good_form=False

    print (request.form['first_name'])
    if len(request.form["first_name"]) < 1:
        flash('First name cannot be blank')
        good_form=False

    print (request.form['last_name'])
    if len(request.form["last_name"]) < 1:
        flash('Last name cannot be blank')
        good_form=False

    print (request.form['pword'])
    if len(request.form["pword"]) < 6:
        good_form=False

    print (request.form['cpword'])
    if len(request.form["cpword"]) < 6:
        good_form=False

    print (request.form['cpword'])
    if request.form["cpword"] != request.form["pword"]:
        flash('Passwords no match')
        good_form=False

    if good_form == False:
        return render_template("register.html", methods=["POST"])
    else:

        query  = mysql.query_db("SELECT * FROM users")

    for i in query:
        if request.form["email"] == i["email"]:
            if request.form["first_name"] == i["first_name"]:
                if request.form["last_name"] == i["last_name"]:
                    if request.form["pword"] == i["pword"]:
                        flash("Success")
            return redirect("/reg")

    second = "INSERT INTO users (email, first_name, last_name, pword) VALUES (%(email)s, %(first_name)s, %(last_name)s, %(pword)s);"
    data = {
            'email': request.form['email'],
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'pword': request.form['pword']
           }
    mysql.query_db(second, data)

    dave = mysql.query_db("SELECT * FROM users")

    if good_form == False:
        return redirect("/reg", methods=["POST"])

    if good_form == True:
        return render_template('dash.html', PLOT=dave, dictionary = pope)


if __name__ == "__main__":
    app.run(debug=True)