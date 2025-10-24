from flask_restful import Api
from flask import Blueprint
from application.controllers.users_controller import UserController, OTPVerifyController, ProfileSetupController,LoginController
from application.controllers.banner_controller import BannerController

user_bp = Blueprint("users", __name__)
user_api = Api(user_bp)

user_api.add_resource(UserController, 'register')
user_api.add_resource(OTPVerifyController, 'verification')
user_api.add_resource(ProfileSetupController, 'profile_setup')
user_api.add_resource(LoginController, 'login')


banner_bp = Blueprint("banners", __name__)
banner_api = Api(banner_bp)
banner_api.add_resource(BannerController, 'banner', 'banner/<int:id>')


def register_routes(app):
    app.register_blueprint(user_bp, url_prefix="/api/users/")
    app.register_blueprint(banner_bp, url_prefix="/api/")
