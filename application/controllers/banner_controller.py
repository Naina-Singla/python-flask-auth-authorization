from flask_restful import Resource
from flask import request, make_response, g
from application.utils.auth_verify import token_required
from datetime import datetime
from application.models.banner import BannerModel
from application.utils.user_role import check_admin
from application.utils.role_checker import role_checker


class BannerController(Resource):
    @token_required
    @role_checker("admin")
    def post(self):
        now = datetime.now()
        try:
            data = request.json
            user_id = g.user_id
            required_fields = ['name', 'desc']
            for item in required_fields:
                if item not in data:
                    return {"message": f"{item} is required", "succcess": False}, 400
            entry_exists = BannerModel.entry_exist(data['name'])
            if entry_exists:
                return {"message": "Banner already added!", "success": False}, 400
            obj = {
                'name': data['name'],
                'desc': data['desc'],
                'created_date': int(now.timestamp()),
                'created_by': user_id,
            }
            save_data = BannerModel(**obj)
            save_data.save_to_db()
            return {"message": "Added Successfully", "success": True}, 201
        except Exception as e:
            message = [str(x) for x in e.args]
            success = False
            return make_response({'success': success,'message': message}, 500)

    @token_required
    @role_checker("admin")
    def patch(self, id):
        now = datetime.now()
        try:
            data = request.json
            user_id = g.user_id
            required_fields = ['name', 'desc']
            for item in required_fields:
                if item not in data:
                    return {"message": f"{item} is required", "succcess": False}, 400
            obj = {
                'id': id,
                'name': data['name'],
                'desc': data['desc'],
                'created_date': int(now.timestamp()),
                'created_by': user_id,
            }
            BannerModel.update_to_db(**obj)
            return {"message": "Updated Successfully", "success": True}, 200
        except Exception as e:
            message = [str(x) for x in e.args]
            success = False
            return make_response({'success': success,'message': message}, 500)

    @token_required
    @role_checker("admin")
    def put(self, id):
        try:
            data = request.json
            user_id = g.user_id
            obj = {
                'id': id,
                'status': data['status']
            }
            BannerModel.update_to_db(**obj)
            return {"message": f"{data['status']} Successfully", "success": True}, 200
        except Exception as e:
            message = [str(x) for x in e.args]
            success = False
            return make_response({'success': success,'message': message}, 500)

    @token_required
    def get(self):
        try:
            search = str(request.args.get("search",))
            limit = int(request.args.get("limit", 10))
            offset = int(request.args.get("offset", 0))
            offset = int(offset) * int(limit)
            
            admin = check_admin(g.user_id)

            if admin.role not in "admin":
                get_data = BannerModel.find_data()
                return {"messsage": "Get Successfully!", "success": True, "count": BannerModel.find_data_count(), "data": get_data}, 200
            get_data_admin = BannerModel.find_data_admin(limit, offset, search)
            return {"messsage": "Get Successfully!", "success": True, "count": BannerModel.find_data_count_admin(search), "data": get_data_admin}, 200
        except Exception as e:
            message = [str(x) for x in e.args]
            success = False
            return make_response({'success': success,'message': message}, 500)

    @token_required
    @role_checker("admin")
    def delete(self, id):
        try:
            record = BannerModel.delete_data(id)
            if record == True:
                return {"message": "Deleted Successfully!", "success": True}, 200
            else:
                return {"message": "No Record Found!", "success": False}, 400
        except Exception as e:
            message = [str(x) for x in e.args]
            success = False
            return make_response({'success': success,'message': message}, 500)