from db import db
from sqlalchemy import text
from application.utils.enums import UserStatus


class BannerModel(db.Model):
    __tablename__ = "banners"

    id= db.Column(db.Integer, primary_key = True, auto_increment = True)
    name = db.Column(db.String(100), nullable = False)
    desc = db.Column(db.String(100), nullable = False)
    created_date = db.Column(db.Integer, nullable = False)
    created_by = db.Column(db.Integer, nullable = False)
    status = db.Column(db.Enum(UserStatus), default = UserStatus.active , nullable = False)

    def __init__(self, **kwargs):
        super(BannerModel, self).__init__(**kwargs)

    def save_to_db(self):
                db.session.add(self)
                db.session.commit()
    @classmethod
    def update_to_db(cls, **data):
        rows_affected = cls.query.filter_by(id=data["id"]).update(data)
        db.session.commit()

    @classmethod
    def entry_exist(cls, name):
        query = text("select * from banners where name = :name")
        res = db.session.execute(query, {'name': name}).mappings().fetchone()
        return res

    @classmethod
    def find_data(cls):
        query = text('select b.name, b.desc from banners b where status = "active"')
        res = db.session.execute(query).mappings().all()
        return [dict(row) for row in res]

    @classmethod
    def find_data_count(cls):
        query = text('select count(*) from banners where status = "active"')
        res = db.session.execute(query).scalar()
        return res
    
    @classmethod
    def find_data_admin(cls, limit, offset, search):
        if search:
            query = text('SELECT * FROM banners where name =:search LIMIT :limit OFFSET :offset')
            res = db.session.execute(query, {'search':search, 'limit': limit, 'offset': offset}).mappings().all()
            return [dict(row) for row in res]
        query = text('SELECT * FROM banners LIMIT :limit OFFSET :offset')
        res = db.session.execute(query, {'search':search, 'limit': limit, 'offset': offset}).mappings().all()
        return [dict(row) for row in res]

    @classmethod
    def find_data_count_admin(cls,search):
        if search:
            query = text('SELECT count(*) FROM banners where name = :search')
            res = db.session.execute(query, {'search':search}).scalar()
            return res
        query = text('SELECT count(*) FROM banners')
        res = db.session.execute(query).scalar()
        return res

    @classmethod
    def delete_data(cls, id):
        record = db.session.get(cls,id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return True
        else: 
            return False
