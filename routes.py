from app import app
from flask import render_template, request, session, redirect, flash
import users, horses, feeds

@app.route("/")

def index():
    user_id = users.user_id()
    print("routes index: user_id=", user_id ) 
    if user_id:
        horse_list = horses.get_ids_and_names()
        feed_list = feeds.get_ids_and_names()
        print("routes index: horse_list=", horse_list , " feed_list=", feed_list )
        return render_template("index.html", horse_list=horse_list, feed_list=feed_list)
    
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

        return redirect("/")
    
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

@app.route("/feed/<feed_id>")
def feed(feed_id):
    user_id = users.user_id()
    feed_name_owner = feeds.get_name_and_owner(feed_id)
    print("routes feed: feed feed_name_owner =", feed_name_owner ) 

    if feed_name_owner == None:
        return render_template("index.html")

    print("routes feed: user_id =", user_id, " vs. owner_id =", feed_name_owner[1])
    
    if user_id != feed_name_owner[1] and feed_name_owner[1]!= 0:
        print("routes feed: not your feed")
        return redirect("/")
    
    nutrition_info = feeds.get_nutriton_info(feed_id)

    if nutrition_info:
        return render_template("feed.html", feed_name=feed_name_owner[0], nutrition_info = nutrition_info)
    else:
        return redirect("/")

@app.route("/newfeed", methods=["GET", "POST"])
def newfeed():
    if request.method == "GET":
        return render_template("newfeed.html")
    
    if request.method == "POST":
        name = request.form["name"]
        moisture = request.form["moisture"]
        energy = request.form["energy"]
        protein = request.form["protein"]
        fat = request.form["fat"]
        fiber = request.form["fiber"]
        starch = request.form["starch"]
        sugar = request.form["sugar"]
        calcium = request.form["calcium"]
        phosphorus = request.form["phosphorus"]
        magnesium = request.form["magnesium"]
        sodium = request.form["sodium"]
        iron = request.form["iron"]
        copper = request.form["copper"]
        manganese = request.form["manganese"]
        zinc = request.form["zinc"]
        iodine = request.form["iodine"]
        selenium = request.form["selenium"]
        cobalt = request.form["cobalt"]
        vitamin_a = request.form["vitamin_a"]
        vitamin_d3 = request.form["vitamin_d3"]
        vitamin_e = request.form["vitamin_e"]
        vitamin_b1 = request.form["vitamin_b1"]
        vitamin_b2 = request.form["vitamin_b2"]
        vitamin_b6 = request.form["vitamin_b6"]
        vitamin_b12 = request.form["vitamin_b12"]
        biotin = request.form["biotin"]
        niacin = request.form["niacin"]

        print("routes newfeed: feed info =", name, moisture, energy, protein ) 

        if not name:
            flash("Please enter the name of the feed!", "error")
            return render_template("newfeed.html")

        added = feeds.add(name, moisture, energy, protein, fat, fiber, starch, sugar, calcium, phosphorus,
                            magnesium, sodium, iron, copper, manganese, zinc, iodine, selenium, cobalt,
                            vitamin_a, vitamin_d3, vitamin_e, vitamin_b1, vitamin_b2, vitamin_b6,
                            vitamin_b12, biotin, niacin)
        if not added:
            flash("Failed to add the feed :(", "error")
            return render_template("newfeed.html")

        return redirect("/")
