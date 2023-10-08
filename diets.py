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
        new_amount = amount[0][0] + int(add_amount)
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


