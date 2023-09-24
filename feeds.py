from db import db
from flask import session
from sqlalchemy.sql import text
import users


def add(name, moisture, energy, protein, fat, fiber, starch, sugar, calcium, phosphorus,
    magnesium, sodium, iron, copper, manganese, zinc, iodine, selenium, cobalt,
    vitamin_a, vitamin_d3, vitamin_e, vitamin_b1, vitamin_b2, vitamin_b6,
    vitamin_b12, biotin, niacin):
    user_id= users.user_id()
    sql = text("""INSERT INTO feeds (
                owner_id, name, moisture, energy, protein, fat, fiber, starch, sugar, calcium, phosphorus,
                magnesium, sodium, iron, copper, manganese, zinc, iodine, selenium, cobalt,
                vitamin_a, vitamin_d3, vitamin_e, vitamin_b1, vitamin_b2, vitamin_b6,
                vitamin_b12, biotin, niacin) 
                VALUES (
                :owner_id, :name, :moisture, :energy, :protein, :fat, :fiber, :starch, :sugar, :calcium, :phosphorus,
                :magnesium, :sodium, :iron, :copper, :manganese, :zinc, :iodine, :selenium, :cobalt,
                :vitamin_a, :vitamin_d3, :vitamin_e, :vitamin_b1, :vitamin_b2, :vitamin_b6,
                :vitamin_b12, :biotin, :niacin)""")
    try:
        db.session.execute(sql, {"owner_id":user_id, "name":name, "moisture":moisture, "energy":energy, 
                                 "protein":protein, "fat": fat, "fiber": fiber, "starch": starch, "sugar": sugar,
                                 "calcium": calcium, "phosphorus": phosphorus, "magnesium": magnesium, "sodium": sodium,
                                 "iron": iron, "copper": copper, "manganese": manganese, "zinc": zinc, "iodine": iodine,
                                 "selenium": selenium, "cobalt": cobalt, "vitamin_a": vitamin_a, "vitamin_d3": vitamin_d3,
                                 "vitamin_e": vitamin_e, "vitamin_b1": vitamin_b1, "vitamin_b2": vitamin_b2, "vitamin_b6": vitamin_b6,
                                 "vitamin_b12": vitamin_b12, "biotin": biotin, "niacin": niacin })

        db.session.commit()
    except:
        print("feeds add: except") 
        return False
    print("feeds add: OK") 
    return True
    
def get_name_and_owner(feed_id):
    sql = text("SELECT name, owner_id FROM feeds WHERE id=:feed_id")
    result = db.session.execute(sql, {"feed_id":feed_id})
    feed = result.fetchone()
    if not feed:
        return None
    return feed

def get_nutrition(reference):
    sql = text("SELECT * FROM nutritions WHERE reference=:reference")
    result = db.session.execute(sql, {"reference":reference})
    nutririon = result.fetchone()
    if not nutririon:
        return None
    return nutririon

def get_ids_and_names():
    user_id = users.user_id()
    sql = text("SELECT id, name FROM feeds") # WHERE (owner_id=:owner_id OR owner_id=0")
    result = db.session.execute(sql) #, {"owner_id": user_id})
    rows = result.fetchall()
    if not rows:
        return None
    else:
        return [(row[0], row[1]) for row in rows]
    

# Tässä olisi tarkotus hakea tietylle rehulle feeds-taulusta vain ne ravintoarvot, jotka eivät ole nollia, 
# ja hakea näille arvoille nimet ja yksiköt nutritions-taulusta, ja palauttaa ne listana tupleja esim. 
# [("Moisture", "M", 50, "%"), ("Metabolizable energy", "ME", 10, "MJ/kg DM"), ("Protein", "DCP", 5, "%" ), ... ]
# Olen yrittänyt koko päivän tehdä sitä jotenkin fiksusti yhdistelemällä SQL-kyselyitä, mutta heikoin tuloksin.
# Voi olla, että joudun tekemään (taas) koko taulujen rakenteen uusiksi.
# Nyt on tällainen versio, että saan edes jotain testattavaa palautettua 2. välipalautukseen.
# Otan tästä mielelläni parannusehdotuksia vastaan, ja jatkan yrittämistä seuraavaan välipalautukseen.

def get_nutriton_info(feed_id):
    sql_feed = text("SELECT * FROM feeds WHERE id=:feed_id")

    result_feed = db.session.execute(sql_feed, {"feed_id": feed_id})
    feed = result_feed.fetchone()
    print("feeds get_nutriton_info: feed = ", feed)
    if not feed:
        return None

    references = result_feed.keys()
    print("feeds get_nutriton_info: references = ", references)

    data = []

    for index, ref in enumerate(references):
        if ref != "id" and ref != "owner_id" and ref != "name":
            sql_nutrition = text("SELECT name, symbol, unit FROM nutritions WHERE reference=:reference")
            result_nutrition = db.session.execute(sql_nutrition, {"reference": ref})
            nutrition= result_nutrition.fetchone()

            if nutrition :
                data.append((nutrition[0], nutrition[1], feed[index], nutrition[2]))

    print("feeds get_nutriton_info: data = ", data)
    return data

