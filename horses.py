from db import db
from flask import session
from sqlalchemy.sql import text
import users

def add(horse_name, birth_year, weight_class, exercise_level):
    user_id= users.user_id()
    sql = text("INSERT INTO horses (horse_name, birth_year, weight_class, exercise_level, owner_id) VALUES (:horse_name, :birth_year, :weight_class, :exercise_level,:owner_id)")
    try:
        db.session.execute(sql, {"horse_name":horse_name, "birth_year":birth_year, "weight_class":weight_class, "exercise_level":exercise_level, "owner_id":user_id })
    except:
        return False
    return True
    
def get_info(horse_id):
    sql = text("SELECT * FROM horses WHERE id=:horse_id")
    result = db.session.execute(sql, {"horse_id":horse_id})
    horse = result.fetchone()
    if not horse:
        return None
    return horse
    
def get_all_ids():
    user_id= users.user_id()
    sql = text("SELECT id FROM horses WHERE owner_id=:owner_id")
    result = db.session.execute(sql, {"owner_id":user_id})
    horse_ids = result.fetchone()
    if not horse_ids:
        return None
    else:
        return horse_ids
    
def get_all_names():
    user_id= users.user_id()
    sql = text("SELECT horse_name FROM horses WHERE owner_id=:owner_id")
    result = db.session.execute(sql, {"owner_id":user_id})
    horse_names = [row[0] for row in result.fetchall()]
    if not horse_names:
        return None
    else:
        return horse_names