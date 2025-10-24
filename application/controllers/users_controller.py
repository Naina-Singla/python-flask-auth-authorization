from flask import request, make_response
from flask_restful import Resource
from application.models.users import OTPModel, UserModel
from application.utils.create_token import create_token
from application.utils.auth_verify import token_required
from datetime import datetime,timedelta
from flask import g
import random
from application.utils.mail import send_mail

class UserController(Resource):
   def post(self):
    data = request.json
    try:
        if not data.get('email'):
            return {"message": "Email is Required", "success": False}, 400

        exist_entry = OTPModel.get_data_by_email(data['email'])
        if exist_entry:
            return {"message": "Email is already registered", "success": False}, 400

        otp_code = random.randint(1000, 9999)
        expiry_time = int((datetime.utcnow() + timedelta(minutes=5)).timestamp())
        send_mail(data['email'], "OTP Verification", str(otp_code))
        obj = {
            "email": data['email'],
            "otp": otp_code,
            "password": data['password'],
            "expires_at": expiry_time
        }

        save_data = OTPModel(**obj)
        save_data.save_to_db()

        return {"message": "Register Successfully!", "success": True}, 200

    except Exception as e:
        message = [str(x) for x in e.args]
        success = False
        return make_response({'success': success, 'message': message}, 500)

class OTPVerifyController(Resource):
    def post(self):
        now = datetime.now()
        try:
            data = request.json
            exist_entry = OTPModel.get_data(data['email'])
            exp = exist_entry[0]['expires_at']
            now = int(now.timestamp())
            print("exp", exp)
            print("now", now)
            if not data.get('otp'):
                return {"message": "OTP is required", "success": False}, 400
            if(exp > now):
                return {"message": "OTP Expired", "success": False}, 400
            if((exist_entry[0]['email'] == data['email']) and (exist_entry[0]['otp'] == data['otp'])):
                print("1")
                profile_data = {
                    "email": exist_entry[0]['email'],
                    "password": exist_entry[0]['password'],
                    "user_id": exist_entry[0]['id'],
                    "created_date" : now,
                }
                print("2")
                save_data = UserModel(**profile_data)
                save_data.save_to_db()
                token = create_token(exist_entry[0]['id'], exist_entry[0]['email'])
                return {"message": "User Verified!", "token": token, "success": True, }, 200
            else:
                return {"message": "Invalid OTP", "success": False}, 400
        except Exception as e:
            message = [str(x) for x in e.args]
            success = False
            return make_response({'success': success,'message': message}, 500)

class ProfileSetupController(Resource):
    @token_required
    def patch(self):
        try:
            data = request.json
            user_id = g.user_id
            find_user = UserModel.find_by_id(user_id)
            required_fields = ["email", "name", "phone", "address"] 
            for item in required_fields:
                if item not in data or not data[item]:
                    return {"message": f"{item} is missing", "success": False}, 400
            obj = {
                "id": find_user[0]['id'],
                "email" : data['email'],
                "name" : data['name'],
                "phone" : data['phone'],
                "address" : data['address'],
            }
            
            UserModel.update_to_db(**obj)
            return {"message": "Profile Updated", "success": True}, 200

        except Exception as e:
            message = [str(x) for x in e.args]
            success = False
            return make_response({'success': success,'message': message}, 500)

class LoginController(Resource):
    def post(self):
        try:
            data = request.json
            exist_entry = UserModel.query.filter_by(email=data['email']).first()
            if exist_entry is None:
                return {"message": "Email not found", "success": True}, 200
            if exist_entry and exist_entry.check_password(data['password']):
                token = create_token(exist_entry.user_id, exist_entry.email)
                return {"message": "Login Successfully!", "success": True, "token": token}, 200
            return {"message": "Email and password are not matched!", "success": False}, 400

        except Exception as e:
            message = [str(x) for x in e.args]
            success = False
            return make_response({'success': success,'message': message}, 500)

