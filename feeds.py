from db import db
from flask import session
from sqlalchemy.sql import text
import users

    
def get_info(feed_id):
    sql = text("SELECT * FROM feeds WHERE id=:feed_id")
    result = db.session.execute(sql, {"feed_id":feed_id})
    feed = result.fetchone()
    if not feed:
        return None
    return feed

def get_ids_and_names():
    user_id = users.user_id()
    sql = text("SELECT id, name FROM feeds WHERE owner_id=:owner_id")
    result = db.session.execute(sql, {"owner_id": 0})
    rows = result.fetchall()
    if not rows:
        return None
    else:
        return [(row[0], row[1]) for row in rows]