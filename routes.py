from app import app
from flask import render_template, request, session, redirect, flash, abort
import users, horses, feeds, diets

@app.route("/")

def index():
    user_id = users.user_id()
    print("routes index: user_id=", user_id ) 
    if user_id:
        horse_list = horses.get_ids_and_names()
        own_feed_list = feeds.get_ids_and_names("own")
        default_feed_list = feeds.get_ids_and_names("default")
        print("routes index: horse_list=", horse_list , " own_feed_list=", own_feed_list )
        return render_template("index.html", horse_list=horse_list, own_feed_list=own_feed_list, default_feed_list = default_feed_list)
    
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
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

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
    feed_list = feeds.get_ids_and_names("all")
    menu = diets.get_info(horse_id)
    nutrition = diets.get_nutrition_table(horse_id)
    if nutrition: 
        ca_p = diets.get_Ca_P(horse_id)
        varying_nutriens = diets.get_horse_specific_nutrients(horse_id)
    else:
        ca_p = None
        varying_nutriens = None

    print("routes horse: horse info =", horse_info ) 
    print("routes horse: menu =", menu )
    if horse_info == None:
        return render_template("index.html")
    
    else:
        print("routes horse: user_id =", user_id, " vs. owner_id =", horse_info[5]) 
        if user_id == horse_info[5]:
            return render_template("horse.html", horse_info=horse_info, feed_list=feed_list, menu=menu, nutrition=nutrition, ca_p=ca_p, varying_nutriens=varying_nutriens)
        else:
            print("routes horse: not the owner")
            return redirect("/")



@app.route("/updatehorse/<horse_id>", methods=["POST"])
def updatehorse(horse_id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    weight_class = request.form["weight_class"]
    exercise_level = request.form["exercise_level"]

    updated = horses.update(horse_id, weight_class, exercise_level)

    if updated:
        print("routes updatehorse: information updated")
    else:
        flash("Failed to update horse information", "error")

    return redirect("/horse/" + horse_id)




@app.route("/deletehorse", methods=['POST'] )
def deletehorse():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    horse_id = request.form["horse_id"]
    deleted = horses.delete(horse_id)

    if deleted:
        return redirect("/")
    else:
        flash("Failed to delete horse from the database", "error")
        return render_template('horse.html', horse_id=horse_id)
    
    




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

    return render_template("feed.html", feed_name=feed_name_owner[0], feed_owner=feed_name_owner[1], feed_id=feed_id, nutrition_info = nutrition_info)


@app.route("/newfeed", methods=["GET", "POST"])
def newfeed():
    if request.method == "GET":
        return render_template("newfeed.html")
    
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        name = request.form["name"]
        moisture = request.form["moisture"].replace(",", ".") or 0
        energy = request.form["energy"].replace(",", ".") or 0
        protein = request.form["protein"].replace(",", ".") or 0
        fat = request.form["fat"].replace(",", ".") or 0
        fiber = request.form["fiber"].replace(",", ".") or 0
        starch = request.form["starch"].replace(",", ".") or 0
        sugar = request.form["sugar"].replace(",", ".") or 0
        calcium = request.form["calcium"].replace(",", ".") or 0
        phosphorus = request.form["phosphorus"].replace(",", ".") or 0
        magnesium = request.form["magnesium"].replace(",", ".") or 0
        sodium = request.form["sodium"].replace(",", ".") or 0
        iron = request.form["iron"].replace(",", ".") or 0
        copper = request.form["copper"].replace(",", ".") or 0
        manganese = request.form["manganese"].replace(",", ".") or 0
        zinc = request.form["zinc"].replace(",", ".") or 0
        iodine = request.form["iodine"].replace(",", ".") or 0
        selenium = request.form["selenium"].replace(",", ".") or 0
        cobalt = request.form["cobalt"].replace(",", ".") or 0
        vitamin_a = request.form["vitamin_a"].replace(",", ".") or 0
        vitamin_d3 = request.form["vitamin_d3"].replace(",", ".") or 0
        vitamin_e = request.form["vitamin_e"].replace(",", ".") or 0
        vitamin_b1 = request.form["vitamin_b1"].replace(",", ".") or 0
        vitamin_b2 = request.form["vitamin_b2"].replace(",", ".") or 0
        vitamin_b6 = request.form["vitamin_b6"].replace(",", ".") or 0
        vitamin_b12 = request.form["vitamin_b12"].replace(",", ".") or 0
        biotin = request.form["biotin"].replace(",", ".") or 0
        niacin = request.form["niacin"].replace(",", ".") or 0
        feed_type = request.form["feed-type"] or "own"

        if users.user_role == 'basic':
            feed_type = "own"

        print("routes newfeed: feed info =", name, moisture, energy, protein ) 

        if not name:
            flash("Please enter the name of the feed!", "error")
            return render_template("newfeed.html")

        added = feeds.add(name, moisture, energy, protein, fat, fiber, starch, sugar, calcium, phosphorus,
                            magnesium, sodium, iron, copper, manganese, zinc, iodine, selenium, cobalt,
                            vitamin_a, vitamin_d3, vitamin_e, vitamin_b1, vitamin_b2, vitamin_b6,
                            vitamin_b12, biotin, niacin, feed_type)
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
    
    feed_old_values = feeds.get_nutrients_for_feed(feed_id)
    print("routes editfeed: feed_old_values =", feed_old_values )
    
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        nutrition = request.form.to_dict()
        nutrition_without_empty_fields = {}

        for nutrient in nutrition:
            if nutrition[nutrient] != "": 
                nutrition_without_empty_fields[nutrient] = nutrition[nutrient].replace(",", ".")
    
        print("routes editfeed: nutrition =" + str(nutrition_without_empty_fields) )

        updated = feeds.update(feed_id, nutrition_without_empty_fields)

        if not updated:
            flash("Failed to update the feed! ", "error")
            return render_template("editfeed.html", feed_name=feed_name_owner[0], feed_old_values=feed_old_values, feed_id=feed_id)
        else:
            flash("Feed updated")
            return redirect("/feed/" + feed_id)
        
    return render_template("editfeed.html", feed_name=feed_name_owner[0], feed_owner=feed_name_owner[1],feed_old_values=feed_old_values, feed_id=feed_id)


@app.route('/add_feed_to_diet/<horse_id>', methods=['POST'])
def add_feed_to_diet(horse_id):
    print("routes add_feed_to_diet: GOT HERE! horse_id = ", horse_id)
    if request.method == 'POST':
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        print("routes add_feed_to_diet: GOT HERE!!!!! POST")
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        feed_id = request.form["feed_id"]
        amount = request.form["amount"].replace(",", ".")

        diets.add(horse_id, feed_id, amount)
        print("routes add_feed_to_diet: horse_id = ", horse_id, ", feed_id = ", feed_id, ", amount = ", amount )

    return redirect("/horse/" + horse_id)


@app.route('/updatediet/<horse_id>', methods= ['POST'] )
def updatediet(horse_id):
    print("routes updatediet: GOT HERE! horse_id = ", horse_id)
    if request.method == 'POST':
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        print("routes updatediet: GOT HERE!!!!! POST")

        feed_id = request.form["feed_id"]
        amount = request.form["amount"].replace(",", ".")

        diets.update(horse_id, feed_id, amount)
        print("routes updatediet: horse_id = ", horse_id, ", feed_id = ", feed_id, ", amount = ", amount )

    return redirect("/horse/" + horse_id)


@app.route('/removefeed/<horse_id>', methods= ['POST'] )
def removefeed(horse_id):
    print("routes removefeed: GOT HERE! horse_id = ", horse_id)
    if request.method == 'POST':
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        feed_id = request.form["feed_id"]
        print("routes removefeed: feed_id = ", feed_id)

        diets.delete(horse_id, feed_id)
        print("routes removefeed: horse_id = ", horse_id, ", feed_id = ", feed_id )

    return redirect("/horse/" + horse_id)

@app.route('/deletefeed', methods= ['POST'] )
def deletefeed():
    
    if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
    
    feed_id = request.form["feed_id"]
    print("routes deletefeed: GOT HERE! feed_id = ", feed_id)
    deleted = feeds.delete(feed_id)
    if deleted:
        print("routes deletefeed: feed_id = ", feed_id)
        return redirect("/")
    else:
        flash("Failed to delete feed from the database", "error")
        return render_template('feed.html', feed_id=feed_id)


@app.route("/admin")
def admin():
    user_role = users.user_role()
    
    if user_role != 'admin':
        print("routes admin: not admin")
        return redirect("/")
    
    else :
        user_list = users.get_all_users()
        return render_template("admin.html", user_list=user_list)
    
@app.route("/update_user_role", methods= ['POST'] )
def update_user_role():
    
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    user_role = users.user_role()
    if user_role != 'admin':
        print("routes admin: not admin")
        flash("Update failed! You do not have rights to edit users.")
    
    else :
        user_to_update = request.form["user_id"]
        new_role = request.form["user_role"]
        updated = users.update_role(user_to_update, new_role)

        if updated:
            user_list = users.get_all_users()

            return render_template("admin.html", user_list=user_list)
        else:
            flash("Failed to update user role", "error")

    return redirect("/admin/")

@app.route("/de_admin_self", methods= ['POST'] )
def de_admin_self():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    user_id = users.user_id()
    updated = users.update_role(user_id, 'basic')

    if updated:
        return redirect("/logout")
    else:
        flash("Failed to update user role", "error")
    
    return redirect("/admin/")

@app.route("/delete_user", methods= ['POST'] )
def delete_user():

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    user_role = users.user_role()
    user_id= users.user_id()
    if user_role != 'admin':
        print("routes delete user: not admin")
        flash("Update failed! You do not have rights to delete users.")
    
    else :
        user_to_delete = request.form["user_id"]
        deleted = users.delete(user_to_delete)

        if deleted:
            
            print("routes delete user: user_id = ", user_id, " user_to_delete = ", user_to_delete)
            if int(user_id) != int(user_to_delete):
                print("routes delete user: HEP!")
                user_list = users.get_all_users()
                return render_template("admin.html", user_list=user_list)
            else:
                
                return redirect("/logout")

        
        else:
            flash("Failed to delete user", "error")

    return redirect("/admin/")