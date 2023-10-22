"""
    This class handles functionality related to the horse's diets.
"""

from db import db
from flask import session
from sqlalchemy.sql import text
import feeds, horses


def add(horse_id, feed_id, add_amount):
    sql = text(
        "SELECT amount FROM diets WHERE horse_id = :horse_id AND feed_id = :feed_id;")

    try:
        result = db.session.execute(
            sql, {"horse_id": horse_id, "feed_id": feed_id})
    except:
        return False

    amount = result.fetchall()

    if not amount:
        return new(horse_id, feed_id, add_amount)
    else:
        new_amount = amount[0][0] + float(add_amount)
        return update(horse_id, feed_id, new_amount)


def new(horse_id, feed_id, amount):
    sql = text(
        "INSERT INTO diets (horse_id, feed_id, amount) VALUES (:horse_id, :feed_id, :amount)")

    try:
        db.session.execute(
            sql, {"horse_id": horse_id, "feed_id": feed_id, "amount": amount})
        db.session.commit()
    except:
        return False
    return True


def update(horse_id, feed_id, amount):
    sql = text(
        "UPDATE diets SET amount = :amount WHERE horse_id = :horse_id AND feed_id = :feed_id;")

    try:
        db.session.execute(
            sql, {"amount": amount, "horse_id": horse_id, "feed_id": feed_id})
        db.session.commit()

    except:
        return False
    return True


def delete(horse_id, feed_id):
    sql = text(
        "DELETE FROM diets WHERE horse_id = :horse_id  AND feed_id = :feed_id;")

    try:
        db.session.execute(sql, {"horse_id": horse_id, "feed_id": feed_id})
        db.session.commit()

    except:
        return False
    return True


def get_info(horse_id):
    sql = text("""SELECT d.feed_id, f.name AS feed_name, d.amount
               FROM diets d JOIN feeds f ON d.feed_id = f.id WHERE d.horse_id = :horse_id""")
    result = db.session.execute(sql, {"horse_id": horse_id})
    diet = result.fetchall()
    if not diet:
        return None

    diet_info = list(diet)
    return diet_info


def get_nutrition_of_diet(horse_id):
    list_of_feeds = get_info(horse_id)
    nutrition_of_diet = []

    if list_of_feeds:
        for feed in list_of_feeds:
            nutrition_of_diet.append(feeds.get_nutrients_for_feed(feed[0]))

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
    result = db.session.execute(sql, {"horse_id": horse_id})
    result_data = result.fetchall()
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
    result = db.session.execute(sql, {"horse_id": horse_id})
    result_data = result.fetchall()
    if not result_data:
        return None

    raw_data = list(result_data[0])

    if len(raw_data) == 0:
        return None

    nutrient_totals = []
    for data in raw_data:
        nutrient_totals.append(format_value(data))

    return nutrient_totals


def get_nutrition_table(horse_id):
    full_nutrition_table = []
    nutrition_table = []

    sql = text("SELECT symbol FROM nutritions")
    result = db.session.execute(sql, {"horse_id": horse_id})
    result_data = list(result.fetchall())
    if not result_data:
        return None
    symbols = [""]
    for symbol in result_data[1:]:
        symbols.append(symbol[0])


    sql = text("SELECT unit FROM nutritions")
    result = db.session.execute(sql, {"horse_id": horse_id})
    result_data = list(result.fetchall())
    if not result_data:
        return None
    units = ["Feeds"]
    for unit in result_data[1:]:
        if unit[0] == "MJ/kg DM":
            units.append("MJ")
        elif unit[0] == "mg/kg":
            units.append("mg")
        elif unit[0] == "IU/kg":
            units.append("IU")
        else:
            units.append("g")

    if not symbols or not units:
        return None

    full_nutrition_table.append(symbols)
    full_nutrition_table.append(units)

    nutrition = get_nutrient_amounts(horse_id)

    if not nutrition:
        return None

    for feed in nutrition:
        full_nutrition_table.append(feed)

    totals = get_nutrient_totals(horse_id)

    if not totals:
        return None
    total = ["Total gain of nutrients"] + totals

    full_nutrition_table.append(total)

    for row in full_nutrition_table:
        nutrition_table.append(row[:3] + row[7:10] + row[11:])

    recommendations = get_recommendations(horse_id)
    if not recommendations:
        return None

    ranges = calculate_ranges(recommendations)
    differences = calculate_differencies(nutrition_table, recommendations)

    nutrition_table.append(ranges)
    nutrition_table.append(differences)

    return nutrition_table


def calculate_differencies(nutrition_table, recommendations):
    differences = ["Difference to the recommendation"]

    for i in range(0, len(recommendations), 2):
        recommendation = float(recommendations[i])
        tolerance = float(recommendations[i + 1])
        value = float(nutrition_table[-1][(i // 2)+1])

        if value - (recommendation - tolerance) < 0:
            difference = format_value(value - (recommendation - tolerance))
        elif value - (recommendation + tolerance) > 0:
            difference = format_value(value - (recommendation + tolerance))
        else:
            difference = 0

        differences.append(float(difference))

    return differences


def calculate_ranges(recommendations):
    ranges = ["Recommended"]

    for i in range(0, len(recommendations), 2):
        recommendation = float(recommendations[i])
        tolerance = float(recommendations[i + 1])

        recommendation_range = "(" + format_value(recommendation - tolerance) + \
            " - " + format_value(recommendation + tolerance) + ")"
        ranges.append(recommendation_range)

    return ranges


def get_recommendations(horse_id):
    horse_info = horses.get_info(horse_id)
    if not horse_info:
        return None
    weight_class = horse_info[3]
    exercise_level = horse_info[4]

    sql = text("""SELECT energy, energy_tolerance,
               protein, protein_tolerance,
               calcium, calcium_tolerance,
               phosphorus, phosphorus_tolerance,
               magnesium, magnesium_tolerance,
               iron, iron_tolerance,
               copper, copper_tolerance,
               manganese, manganese_tolerance,
               zinc, zinc_tolerance,
               iodine, iodine_tolerance,
               selenium, selenium_tolerance,
               cobalt, cobalt_tolerance,
               vitamin_a, vitamin_a_tolerance,
               vitamin_d3, vitamin_d3_tolerance,
               vitamin_e, vitamin_e_tolerance,
               vitamin_b1, vitamin_b1_tolerance,
               vitamin_b2, vitamin_b2_tolerance,
               vitamin_b6, vitamin_b6_tolerance,
               vitamin_b12, vitamin_b12_tolerance,
               biotin, biotin_tolerance,
               niacin, niacin_tolerance
               FROM recommendations WHERE weight_class = :weight_class
               AND exercise_level = :exercise_level;""")

    try:
        result = db.session.execute(
            sql, {"weight_class": weight_class, "exercise_level": exercise_level})
    except:
        return None

    recommendations = list(result.fetchall()[0])
    if not recommendations:
        return None

    return recommendations


def format_value(value):

    number = float(value)
    
    if number.is_integer():
        return str(int(number))
    elif abs(number) >= 100:
        return "{:.0f}".format(number)
    elif abs(number) > 1:
        return "{:.1f}".format(number)
    elif 0.1 <= abs(number) < 1:
        return "{:.2f}".format(number)
    elif 0.01 <= abs(number) < 0.1:
        return "{:.3f}".format(number)
    elif 0.001 <= abs(number) < 0.01:
        return "{:.4f}".format(number)
    else:
        return "{:.5f}".format(number)


def get_ca_p(horse_id):
    sql = text("""SELECT
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.calcium) AS total_calcium,
                SUM((d.amount - (d.amount * f.moisture / 100)) * f.phosphorus) AS total_phosphorus
                FROM diets d JOIN feeds f ON d.feed_id = f.id WHERE d.horse_id = :horse_id;""")
    result = db.session.execute(sql, {"horse_id": horse_id})
    result_data = result.fetchall()
    if not (result_data[0][0] and result_data[0][1]):
        return None

    calsium = float(result_data[0][0])
    phosphorus = float(result_data[0][1])

    if phosphorus == 0:
        relation = 0
    else:
        relation = round(calsium / phosphorus, 1)

    if relation < 1.2:
        difference = round(relation - 1.2, 1)
    elif relation > 1.8:
        difference = round(relation - 1.8, 1)
    else:
        difference = 0

    ca_p = [relation, difference]
    return ca_p


def get_horse_specific_nutrients(horse_id):
    totals = get_nutrient_totals(horse_id)
    if not totals:
        return None

    return totals[2:6]
