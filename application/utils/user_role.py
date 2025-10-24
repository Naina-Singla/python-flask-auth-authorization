from db import db
from sqlalchemy import text

def check_admin(user_id):
    query = text("select * from users where user_id = :user_id")
    res = db.session.execute(query, {'user_id': user_id}).mappings().fetchone()
    return res