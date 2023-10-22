from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

def login(username, password):
    sql = text("SELECT id, username, role, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role
            print("users login: id=", session["user_id"], ", username=", session["username"], ", role=", session["role"]) 
            return True
        else:
            return False

def logout():
    print("users logout: id=", session["user_id"], ", username=", session["username"], ", role=", session["role"])    
    session.clear()


def register(username, password):
    hash_value = generate_password_hash(password)
    role ='basic'
    try:
        sql = text("INSERT INTO users (username,password,role) VALUES (:username,:password,:role)")
        db.session.execute(sql, {"username":username, "password":hash_value, "role":role })
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id",0)

def user_role():
    return session.get("role",'basic')

def get_all_users():
    id = user_id()
    sql = text("SELECT id, username, role FROM users WHERE id !=:id ORDER BY id")
    result = db.session.execute(sql, {"id": id})
    users = result.fetchall()
    if not users:
        return None
    else:
        return list(users)

def update_role(user_to_update, new_role):
    if user_role() != 'admin':
        return False
    
    sql = text("UPDATE users SET role =:new_role WHERE id = :user_to_update")
    try:
        db.session.execute(sql, {"new_role": new_role, "user_to_update": user_to_update})
        db.session.commit()
    except:
        print("user role update: except") 
        return False
    
    print("user role update: OK") 
    return True

def delete(user_to_delete):
    if user_role() != 'admin':
        return False
    
    sql_feeds = text("DELETE FROM feeds WHERE owner_id = :user_to_delete")
    sql_user = text("DELETE FROM users WHERE id = :user_to_delete")
    try:
        db.session.execute(sql_feeds, {"user_to_delete": user_to_delete})
        db.session.execute(sql_user, {"user_to_delete": user_to_delete})
        db.session.commit()
    except:
        print("user delete: except") 
        return False
    
    print("user role delete: OK") 
    return True