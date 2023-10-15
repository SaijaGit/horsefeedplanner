from db import db
from flask import session
from sqlalchemy.sql import text
import users, feeds, horses

def add(horse_id, feed_id, add_amount):
    sql = text("SELECT amount FROM diets WHERE horse_id = :horse_id AND feed_id = :feed_id;")
    print("diets add: sql =", sql, {"horse_id":horse_id, "feed_id":feed_id} ) 
    try:
        result = db.session.execute(sql, {"horse_id":horse_id, "feed_id":feed_id})
    except:
        print("diets add: except") 
        return False
    
    amount = result.fetchall()
    print("diets add: amount =", amount) 
    if not amount:
        return new(horse_id, feed_id, add_amount)
    
    else :
        new_amount = amount[0][0] + float(add_amount)
        return update(horse_id, feed_id, new_amount)


def new(horse_id, feed_id, amount):
    sql = text("INSERT INTO diets (horse_id, feed_id, amount) VALUES (:horse_id, :feed_id, :amount)")
    print("diets new: sql =", sql, {"horse_id":horse_id, "feed_id":feed_id, "amount":amount} )
    try:
        db.session.execute(sql, {"horse_id":horse_id, "feed_id":feed_id, "amount":amount })
        db.session.commit()
    except:
        print("diets add: except") 
        return False
    print("diets add: OK") 
    return True

def update(horse_id, feed_id, amount):
    sql = text("UPDATE diets SET amount = :amount WHERE horse_id = :horse_id AND feed_id = :feed_id;")
    print("diets update: sql =", sql, {"amount":amount, "horse_id":horse_id, "feed_id":feed_id })

    try:
        db.session.execute(sql, {"amount":amount, "horse_id":horse_id, "feed_id":feed_id })
        db.session.commit()

    except:
        print("diets update: except") 
        return False
    print("diets update: OK") 
    return True



def delete(horse_id, feed_id):
    sql = text("DELETE FROM diets WHERE horse_id = :horse_id  AND feed_id = :feed_id;")
    print("diets delete: sql =", sql, {"horse_id":horse_id, "feed_id":feed_id })

    try:
        db.session.execute(sql, {"horse_id":horse_id, "feed_id":feed_id })
        db.session.commit()

    except:
        print("diets delete: except") 
        return False
    print("diets delete: OK") 
    return True


def get_info(horse_id):
    sql = text("SELECT d.feed_id, f.name AS feed_name, d.amount FROM diets d JOIN feeds f ON d.feed_id = f.id WHERE d.horse_id = :horse_id")
    result = db.session.execute(sql, {"horse_id":horse_id})
    diet= result.fetchall()
    if not diet:
        return None

    diet_info = list(diet)
    print("diets get_info: diet_info = ", diet_info)
    return diet_info


def get_nutrition_of_diet(horse_id):
    list_of_feeds = get_info(horse_id)
    nutrition_of_diet = []

    if list_of_feeds: 
        for feed in list_of_feeds:
            nutrition_of_diet.append(feeds.get_nutrients_for_feed(feed[0]))
    
        print("diets get_nutrition_of_diet: ",  nutrition_of_diet)
    
    return nutrition_of_diet

def get_nutrient_amounts(horse_id):
    sql = text("""SELECT f.name AS feed_name,
                (d.amount - (d.amount * f.moisture / 100)) * f.energy AS total_energy,
                (d.amount - (d.amount * f.moisture / 100)) * 10 * f.protein AS total_protein,
                (d.amount - (d.amount * f.moisture / 100)) * 10 *  f.fat AS total_fat,
                (d.amount - (d.amount * f.moisture / 100)) * 10 *  f.fiber AS total_fiber,
                (d.amount - (d.amount * f.moisture / 100)) * 10 *  f.starch AS total_starch,
                (d.amount - (d.amount * f.moisture / 100)) * 10 *  f.sugar AS total_sugar,
                (d.amount - (d.amount * f.moisture / 100)) * f.calcium AS total_calcium,
                (d.amount - (d.amount * f.moisture / 100)) * f.phosphorus AS total_phosphorus,
                (d.amount - (d.amount * f.moisture / 100)) * f.magnesium AS total_magnesium,
                (d.amount - (d.amount * f.moisture / 100)) * f.sodium AS total_sodium,
                (d.amount - (d.amount * f.moisture / 100)) * f.iron AS total_iron,
                (d.amount - (d.amount * f.moisture / 100)) * f.copper AS total_copper,
                (d.amount - (d.amount * f.moisture / 100)) * f.manganese AS total_manganese,
                (d.amount - (d.amount * f.moisture / 100)) * f.zinc AS total_zinc,
                (d.amount - (d.amount * f.moisture / 100)) * f.iodine AS total_iodine,
                (d.amount - (d.amount * f.moisture / 100)) * f.selenium AS total_selenium,
                (d.amount - (d.amount * f.moisture / 100)) * f.cobalt AS total_cobalt,
                (d.amount - (d.amount * f.moisture / 100)) * f.vitamin_a AS total_vitamin_a,
                (d.amount - (d.amount * f.moisture / 100)) * f.vitamin_d3 AS total_vitamin_d3,
                (d.amount - (d.amount * f.moisture / 100)) * f.vitamin_e AS total_vitamin_e,
                (d.amount - (d.amount * f.moisture / 100)) * f.vitamin_b1 AS total_vitamin_b1,
                (d.amount - (d.amount * f.moisture / 100)) * f.vitamin_b2 AS total_vitamin_b2,
                (d.amount - (d.amount * f.moisture / 100)) * f.vitamin_b6 AS total_vitamin_b6,
                (d.amount - (d.amount * f.moisture / 100)) * f.vitamin_b12 AS total_vitamin_b12,
                (d.amount - (d.amount * f.moisture / 100)) * f.biotin AS total_biotin,
                (d.amount - (d.amount * f.moisture / 100)) * f.niacin AS total_niacin
                FROM diets d JOIN feeds f ON d.feed_id = f.id WHERE d.horse_id = :horse_id;""")
    result = db.session.execute(sql, {"horse_id":horse_id})
    result_data= result.fetchall()
    if not result_data:
        return None

    raw_data = list(result_data)

    nutrient_amounts = []
    for i in range(len(raw_data)):
        for j in range(len(raw_data[i])):
            if j == 0:
                row = [raw_data[i][0]]
            else:
                row.append(format_value(raw_data[i][j]))
        nutrient_amounts.append(row)


    
    print("diets get_nutrient_amounts: nutrient_amounts = ", nutrient_amounts)
    return nutrient_amounts

def get_nutrient_totals(horse_id):
    sql = text("""SELECT
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.energy) AS total_energy,
                SUM((d.amount - (d.amount * f.moisture / 100)) * 10 *  f.protein) AS total_protein,
                SUM((d.amount - (d.amount * f.moisture / 100)) * 10 *  f.fat) AS total_fat,
                SUM((d.amount - (d.amount * f.moisture / 100)) * 10 *  f.fiber) AS total_fiber,
                SUM((d.amount - (d.amount * f.moisture / 100)) * 10 *  f.starch) AS total_starch,
                SUM((d.amount - (d.amount * f.moisture / 100)) * 10 *  f.sugar) AS total_sugar,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.calcium) AS total_calcium,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.phosphorus) AS total_phosphorus,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.magnesium) AS total_magnesium,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.sodium) AS total_sodium,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.iron) AS total_iron,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.copper) AS total_copper,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.manganese) AS total_manganese,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.zinc) AS total_zinc,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.iodine) AS total_iodine,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.selenium) AS total_selenium,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.cobalt) AS total_cobalt,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.vitamin_a) AS total_vitamin_a,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.vitamin_d3) AS total_vitamin_d3,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.vitamin_e) AS total_vitamin_e,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.vitamin_b1) AS total_vitamin_b1,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.vitamin_b2) AS total_vitamin_b2,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.vitamin_b6) AS total_vitamin_b6,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.vitamin_b12) AS total_vitamin_b12,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.biotin) AS total_biotin,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.niacin) AS total_niacin
                FROM diets d JOIN feeds f ON d.feed_id = f.id WHERE d.horse_id = :horse_id;""")
    result = db.session.execute(sql, {"horse_id":horse_id})
    result_data= result.fetchall()
    if not result_data:
        return None

    raw_data = list(result_data[0])

    nutrient_totals = []
    for data in raw_data:
        nutrient_totals.append(format_value(data))
    print("diets get_nutrient_totals: nutrient_totals = ", nutrient_totals)
    return nutrient_totals


def get_nutrition_table(horse_id):
    nutrition_table = []
    sql = text("SELECT symbol FROM nutritions")
    result = db.session.execute(sql, {"horse_id":horse_id})
    result_data = list(result.fetchall())
    if not result_data:
        return None
    symbols = [""]
    for symbol in result_data[1:]:
        symbols.append(symbol[0])
    print("!!!! diets get_nutrition_table: symbols = ",  symbols)

    sql = text("SELECT unit FROM nutritions")
    result = db.session.execute(sql, {"horse_id":horse_id})
    result_data= list(result.fetchall())
    if not result_data:
        return None
    units= ["Feeds"]
    for unit in result_data[1:]:
        if unit[0] == "MJ/kg DM":
            units.append("MJ")
        elif unit[0] == "mg/kg":
            units.append("mg")
        elif unit[0] == "IU/kg":
            units.append("IU")
        else :
            units.append("g")
    print("!!!! diets get_nutrition_table: units = ",  units)

    if not symbols or not units:
        return None
    
    nutrition_table.append(symbols)
    nutrition_table.append(units)

    nutrition = get_nutrient_amounts(horse_id)
    print("!!!!!!!!!!!! diets get_nutrition_table: nutrition = ",  nutrition)
    if not nutrition:
        return None
    
    for feed in nutrition:
        nutrition_table.append(feed)

    
    totals = get_nutrient_totals(horse_id)
    print("!!!! diets get_nutrition_table: totals = ",  totals)
    if not totals:
        return None
    total = ["Total gain of nutrients"] + totals

    nutrition_table.append(total)

    print("diets get_nutrition_table: nutrition_table = ",  nutrition_table)

    return nutrition_table

def format_value(value):
    print("diets format_value: value *1 = ",  value)
    number = float(value)
    print("diets format_value: number *1 = ",  number)
    if number.is_integer():
        print("diets format_value: number *2 = ",  str(int(number)))
        return str(int(number))
    elif number > 1:
        print("diets format_value: number *3 = ",  "{:.1f}".format(number))
        return "{:.1f}".format(number)
    elif 0.1 <= number < 1:
        print("diets format_value: number *4 = ",  "{:.1f}".format(number))
        return "{:.2f}".format(number)
    elif 0.01 <= number < 0.1:
        return "{:.3f}".format(number)
    elif 0.001 <= number < 0.01:
        return "{:.4f}".format(number)
    elif number < 0.001:
        return "{:.5f}".format(number)



def get_Ca_P(horse_id):
    sql = text("""SELECT
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.calcium) AS total_calcium,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.phosphorus) AS total_phosphorus
                FROM diets d JOIN feeds f ON d.feed_id = f.id WHERE d.horse_id = :horse_id;""")
    result = db.session.execute(sql, {"horse_id":horse_id})
    result_data= result.fetchall()
    if not (result_data[0][0] and result_data[0][1]):
        return None
    
    print("diets calculate_Ca_P: calsium = ", result_data[0][0], ", phosphorus = ", result_data[0][1])

    calsium = float(result_data[0][0])
    phosphorus = float(result_data[0][1])
    ca_p = format_value(calsium / phosphorus)

    print("diets calculate_Ca_P: calsium = ", calsium, ", phosphorus = ", phosphorus, "Ca/P = ", ca_p)
    return ca_p


def calculate_sugar(horse_id):
    return horse_id