from functools import wraps
import jwt
import os
from dotenv import load_dotenv
from flask import request, g
load_dotenv()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization", None)

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return {"message": "Token is missing!"}, 401
        try:
            secret_key = os.getenv("SECRET_KEY")
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            g.user = data  
            g.user_id = data.get("user_id") 
        except jwt.ExpiredSignatureError:
            return {"message": "Token has expired!"}, 401
        except jwt.InvalidTokenError:
            return {"message": "token111!"}, 401

        return f(*args, **kwargs)
    return decorated