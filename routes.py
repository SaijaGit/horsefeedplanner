from app import app
from flask import render_template, request, session, redirect, flash
import users, horses

@app.route("/")

def index():
    user_id = users.user_id()
    print("routes index: user_id=", user_id ) 
    if user_id:
        horse_list = horses.get_ids_and_names()
        print("routes index: horse_info=", horse_list )
        return render_template("index.html", horse_list=horse_list)
    
    else:
        return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            flash("Incorrect username or password!", "error")
            return render_template("login.html")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            flash("Passwords don't match!", "error")
            return render_template("register.html")
        if users.register(username, password1):
            return redirect("/")
        else:
            flash("Account creation failed:(", "error")
            return render_template("register.html")
        
@app.route("/newhorse", methods=["GET", "POST"])
def newhorse():
    if request.method == "GET":
        return render_template("newhorse.html")
    
    if request.method == "POST":
        horse_name = request.form["horse_name"]
        birth_year = request.form["birth_year"]
        weight_class = request.form["weight_class"]
        exercise_level = request.form["exercise_level"]
        print("routes newhorse: horse info =", horse_name, birth_year, weight_class, exercise_level ) 

        if not horse_name or not birth_year or not weight_class or not exercise_level:
            flash("Please fill in all the required fields!", "error")
            return render_template("newhorse.html")

        added = horses.add(horse_name, birth_year, weight_class, exercise_level)
        if not added:
            flash("Failed to add the horse :(", "error")
            return render_template("newhorse.html")
        
        horse_names = horses.get_all_names()
        return render_template("index.html", horse_names=horse_names)
    
@app.route("/horse/<horse_id>")
def horse(horse_id):
    user_id = users.user_id()
    horse_info = horses.get_info(horse_id)
    print("routes horse: horse info =", horse_info ) 
    if horse_info == None:
        return render_template("index.html")
    
    else:
        print("routes horse: user_id =", user_id, " vs. owner_id =", horse_info[5]) 
        if user_id == horse_info[5]:
            return render_template("horse.html", horse_info=horse_info)
        else:
            print("routes horse: not the owner")
            return redirect("/")
