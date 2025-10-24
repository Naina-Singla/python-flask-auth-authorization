import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def create_token(user_id, email):
    payload = {
        "user_id" : user_id,
        "email": email,
        "exp" :datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat" : datetime.datetime.utcnow() 
    }
    secret_key = os.getenv('SECRET_KEY')
    try:
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        return token
    except Exception as e:
        return None