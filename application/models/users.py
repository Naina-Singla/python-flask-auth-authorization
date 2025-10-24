from db import db
from sqlalchemy import text
from application.utils.enums import UserRole, UserStatus
from werkzeug.security import generate_password_hash, check_password_hash

class OTPModel(db.Model):
    __tablename__ = "register"

    id= db.Column(db.Integer, primary_key = True, auto_increment = True)
    email = db.Column(db.String(20), nullable = False)
    otp = db.Column(db.Integer, nullable =False)
    password = db.Column("password", db.String(255), nullable= False)
    expires_at = db.Column(db.Integer, nullable =False)

    def __init__(self, **kwargs):
        super(OTPModel, self).__init__(**kwargs)

    def save_to_db(self):
                db.session.add(self)
                db.session.commit()
    @classmethod
    def update_to_db(cls, **data):
        rows_affected = cls.query.filter_by(id=data["id"]).update(data)
        db.session.commit()

    @classmethod
    def get_data(cls, email):
        query = text('select * from register where email =:email')
        res = db.session.execute(query, {'email': email}).mappings().all()
        return res
    
    @classmethod
    def get_data_by_email(cls, email):
        query = text('select * from register where email =:email')
        res = db.session.execute(query, {'email': email}).first()
        return res

class UserModel(db.Model):
    __tablename__ = "users"

    id= db.Column(db.Integer, primary_key = True, auto_increment = True)
    email = db.Column(db.String(20), nullable = False)
    name = db.Column(db.String(20), nullable = False)
    phone = db.Column(db.String(20), nullable = False)
    address = db.Column(db.String(50), nullable = False)
    role = db.Column(db.Enum(UserRole), default=UserRole.user, nullable=False)
    status = db.Column(db.Enum(UserStatus), default=UserStatus.active, nullable=False)
    created_date = db.Column(db.String(50), nullable = False)
    user_id = db.Column(db.Integer, nullable = False)
    _password = db.Column("password",db.String(255), nullable=False)

    @property
    def password(self):
        raise AttributeError("Password is write-only")

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password, method="pbkdf2:sha256")

    def check_password(self, raw_password):
        return check_password_hash(self._password, raw_password)

    def __init__(self, **kwargs):
        super(UserModel, self).__init__(**kwargs)

    def save_to_db(self):
                db.session.add(self)
                db.session.commit()
    @classmethod
    def update_to_db(cls, **data):
        rows_affected = cls.query.filter_by(id=data["id"]).update(data)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        query = text('select * from users where user_id = :id')
        res = db.session.execute(query, {"id": id}).mappings().all()
        return res
    
    @classmethod
    def find_by_email(cls, email):
        query = text("select * from users where email = :email")
        res = db.session.execute(query, {"email": email}).mappings().all()
        return res
