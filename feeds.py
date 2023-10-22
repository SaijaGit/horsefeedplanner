"""
    This class handles the nutrition information of the feeds.
    It retrieves and adds nutritional information to the database, and compiles the information into a suitable format for an html page.
"""

from db import db
from sqlalchemy.sql import text
import users


def add(name, moisture, energy, protein, fat, fiber, starch, sugar, calcium, phosphorus,
        magnesium, sodium, iron, copper, manganese, zinc, iodine, selenium, cobalt,
        vitamin_a, vitamin_d3, vitamin_e, vitamin_b1, vitamin_b2, vitamin_b6,
        vitamin_b12, biotin, niacin, feed_type):

    if feed_type == "default":
        owner_id = 0
    else:
        owner_id = users.user_id()

    if float(moisture) > 100:
        moisture = "100"

    sql = text("""INSERT INTO feeds (
               owner_id, name, moisture, energy, protein, fat,
               fiber, starch, sugar, calcium, phosphorus,
               magnesium, sodium, iron, copper, manganese,
               zinc, iodine, selenium, cobalt, vitamin_a,
               vitamin_d3, vitamin_e, vitamin_b1, vitamin_b2,
               vitamin_b6, vitamin_b12, biotin, niacin) 
               VALUES (
               :owner_id, :name, :moisture, :energy, :protein,
               :fat, :fiber, :starch, :sugar, :calcium,
               :phosphorus, :magnesium, :sodium, :iron,
               :copper, :manganese, :zinc, :iodine, :selenium,
               :cobalt,:vitamin_a, :vitamin_d3, :vitamin_e,
               :vitamin_b1, :vitamin_b2, :vitamin_b6,
               :vitamin_b12, :biotin, :niacin)""")
    try:
        db.session.execute(sql, {"owner_id": owner_id,
                                 "name": name,
                                 "moisture": moisture,
                                 "energy": energy,
                                 "protein": protein,
                                 "fat": fat,
                                 "fiber": fiber,
                                 "starch": starch,
                                 "sugar": sugar,
                                 "calcium": calcium,
                                 "phosphorus": phosphorus,
                                 "magnesium": magnesium,
                                 "sodium": sodium,
                                 "iron": iron,
                                 "copper": copper,
                                 "manganese": manganese,
                                 "zinc": zinc,
                                 "iodine": iodine,
                                 "selenium": selenium,
                                 "cobalt": cobalt,
                                 "vitamin_a": vitamin_a,
                                 "vitamin_d3": vitamin_d3,
                                 "vitamin_e": vitamin_e,
                                 "vitamin_b1": vitamin_b1,
                                 "vitamin_b2": vitamin_b2,
                                 "vitamin_b6": vitamin_b6,
                                 "vitamin_b12": vitamin_b12,
                                 "biotin": biotin,
                                 "niacin": niacin})
        db.session.commit()
    except:
        return False

    return True


def update(feed_id, nutrition):
    user_id = users.user_id()
    user_role = users.user_role()
    nutrients_to_update = []
    owner_id = get_name_and_owner(feed_id)[1]

    if user_id == owner_id or (owner_id == 0 and user_role == 'admin'):

        for nutrient, value in nutrition.items():
            nutrients_to_update.append(f"{nutrient} = :{nutrient}")

        if len(nutrients_to_update) == 0:
            return False

        sql_nutrients = ", ".join(nutrients_to_update)
        sql = text(
            f"""UPDATE feeds SET {sql_nutrients} WHERE id = :feed_id;""")

        try:
            db.session.execute(sql,  {"feed_id": feed_id, **nutrition})
            db.session.commit()
        except:
            return False

        return True

    else:
        return False


def delete(feed_id):
    user_id = users.user_id()
    user_role = users.user_role()
    owner_id = get_name_and_owner(feed_id)[1]

    if user_id == owner_id or (owner_id == 0 and user_role == 'admin'):
        sql = text("DELETE FROM feeds WHERE id=:feed_id")
        try:
            db.session.execute(sql, {"feed_id": feed_id})
            db.session.commit()
        except:
            return False
        return True
    else:
        return False


def get_name_and_owner(feed_id):
    sql = text("SELECT name, owner_id FROM feeds WHERE id=:feed_id")
    result = db.session.execute(sql, {"feed_id": feed_id})
    feed = result.fetchone()
    return feed


def get_nutrition(reference):
    sql = text("""SELECT reference, name, symbol, unit, description
               FROM nutritions WHERE reference=:reference""")
    result = db.session.execute(sql, {"reference": reference})
    nutririon = result.fetchone()
    return nutririon


def get_ids_and_names(whose="own"):
    user_id = users.user_id()
    if whose == "own":
        sql = text("SELECT id, name FROM feeds WHERE owner_id=:user_id")
    elif whose == "default":
        sql = text("SELECT id, name FROM feeds WHERE owner_id=0")
    elif whose == "all":
        sql = text(
            "SELECT id, name FROM feeds WHERE owner_id=:user_id OR owner_id=0")
    else:
        return None

    result = db.session.execute(sql, {"user_id": user_id})
    rows = result.fetchall()
    if not rows:
        return None
    else:
        return [(row[0], row[1]) for row in rows]


def get_nutrients_for_feed(feed_id):
    sql_feed = text("""SELECT name, moisture, energy, protein, fat, fiber, starch, 
                    sugar, calcium, phosphorus, magnesium, sodium, iron, copper, manganese, 
                    zinc, iodine, selenium, cobalt, vitamin_a, vitamin_d3, vitamin_e, 
                    vitamin_b1, vitamin_b2, vitamin_b6, vitamin_b12,  biotin, niacin 
                    FROM feeds WHERE id=:feed_id""")

    result_feed = db.session.execute(sql_feed, {"feed_id": feed_id})
    feed = result_feed.fetchone()

    return feed


def get_nutrition_info(feed_id):
    sql_feed = text("""SELECT moisture, energy, protein, fat, fiber, starch, 
                    sugar, calcium, phosphorus, magnesium, sodium, iron, copper, 
                    manganese, zinc, iodine, selenium, cobalt, vitamin_a, vitamin_d3, 
                    vitamin_e, vitamin_b1, vitamin_b2, vitamin_b6, vitamin_b12, biotin, 
                    niacin FROM feeds WHERE id=:feed_id""")

    result_feed = db.session.execute(sql_feed, {"feed_id": feed_id})
    feed = result_feed.fetchone()

    if not feed:
        return None

    references = result_feed.keys()
    data = []

    for index, ref in enumerate(references):
        if ref != "id":
            sql_nutrition = text(
                "SELECT name, symbol, unit FROM nutritions WHERE reference=:reference")
            result_nutrition = db.session.execute(
                sql_nutrition, {"reference": ref})
            nutrition = result_nutrition.fetchone()

            if nutrition:
                if feed[index] != 0:
                    data.append(
                        (nutrition[0], nutrition[1], feed[index], nutrition[2]))

    return data
