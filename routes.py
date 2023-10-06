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


# routes.py

@app.route("/updatehorse/<horse_id>", methods=["POST"])
def updatehorse(horse_id):

    weight_class = request.form["weight_class"]
    exercise_level = request.form["exercise_level"]

    updated = horses.update(horse_id, weight_class, exercise_level)

    if updated:
        print("routes updatehorse: information updated")
        flash("Horse information updated successfully", "success")
    else:
        flash("Failed to update horse information", "error")

    return redirect("/horse/" + horse_id)


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
    
    nutrition_info = feeds.get_nutrition_info(feed_id)

    return render_template("feed.html", feed_name=feed_name_owner[0], feed_id=feed_id, nutrition_info = nutrition_info)

    #if nutrition_info:
    #    return render_template("feed.html", feed_name=feed_name_owner[0], nutrition_info = nutrition_info)
    #else:
    #    return redirect("/")

@app.route("/newfeed", methods=["GET", "POST"])
def newfeed():
    if request.method == "GET":
        return render_template("newfeed.html")
    
    if request.method == "POST":
        name = request.form["name"]
        moisture = request.form["moisture"] or 0
        energy = request.form["energy"] or 0
        protein = request.form["protein"] or 0
        fat = request.form["fat"] or 0
        fiber = request.form["fiber"] or 0
        starch = request.form["starch"] or 0
        sugar = request.form["sugar"] or 0
        calcium = request.form["calcium"] or 0
        phosphorus = request.form["phosphorus"] or 0
        magnesium = request.form["magnesium"] or 0
        sodium = request.form["sodium"] or 0
        iron = request.form["iron"] or 0
        copper = request.form["copper"] or 0
        manganese = request.form["manganese"] or 0
        zinc = request.form["zinc"] or 0
        iodine = request.form["iodine"] or 0
        selenium = request.form["selenium"] or 0
        cobalt = request.form["cobalt"] or 0
        vitamin_a = request.form["vitamin_a"] or 0
        vitamin_d3 = request.form["vitamin_d3"] or 0
        vitamin_e = request.form["vitamin_e"] or 0
        vitamin_b1 = request.form["vitamin_b1"] or 0
        vitamin_b2 = request.form["vitamin_b2"] or 0
        vitamin_b6 = request.form["vitamin_b6"] or 0
        vitamin_b12 = request.form["vitamin_b12"] or 0
        biotin = request.form["biotin"] or 0
        niacin = request.form["niacin"] or 0

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

@app.route("/editfeed/<feed_id>", methods=["GET", "POST"])
def editfeed(feed_id):
    user_id = users.user_id()
    feed_name_owner = feeds.get_name_and_owner(feed_id)

    if user_id != feed_name_owner[1] and feed_name_owner[1] != 0:
        print("routes editfeed: not the owner, user_id =" + user_id + ",  feed_name_owner =" + feed_name_owner)
        return redirect("/")
    
    nutrition_info = feeds.get_nutrition_info(feed_id)
    
    if request.method == "POST":

        nutrition = request.form.to_dict()
        nutrition_without_empty_fields = {}

        for nutrient in nutrition:
            if nutrition[nutrient] != "": 
                nutrition_without_empty_fields[nutrient] = nutrition[nutrient]
    
        print("routes editfeed: nutrition =" + str(nutrition_without_empty_fields) )

        updated = feeds.update(feed_id, nutrition_without_empty_fields)

        if not updated:
            flash("Failed to update the feed :(", "error")
            return render_template("editfeed.html", feed_name=feed_name_owner[0], nutrition_info=nutrition_info, feed_id=feed_id)
        else:
            flash("Feed updated")
            return redirect("/feed/" + feed_id)
        
    return render_template("editfeed.html", feed_name=feed_name_owner[0], nutrition_info=nutrition_info, feed_id=feed_id)
    