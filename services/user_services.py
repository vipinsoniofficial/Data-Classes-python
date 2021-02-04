import marshmallow_dataclass

from config import db,session1
from models.user_models import TheLanguage


class Work:
    @property
    def get_all_user(self):
        try:
            users_list = []
            all_users = TheLanguage.query.all()
            schema = marshmallow_dataclass.class_schema(TheLanguage)
            for i in all_users:
                users_list.append(schema().dump(i))
            print(schema().dump(all_users, many=True))
            return users_list
        except Exception:
            raise Exception("Issue in finding user")

    def add_new_user(self, data):
        try:
            schema = marshmallow_dataclass.class_schema(TheLanguage)
            new_language = schema().load(data)
            # print("new language:", new_language, type(new_language))

            session1.add(new_language)
            session1.commit()
            return {'result': 'Language added'}, 201
        except Exception:
            raise Exception("Issue in adding user")

    def get_user_by_id(self, id):
        try:
            user = TheLanguage.query.filter_by(id=id).first()
            schema = marshmallow_dataclass.class_schema(TheLanguage)
            result_db = schema().dump(user)
            return result_db
        except Exception:
            raise Exception("Issue in getting user")

    def update_user_data(self, id, data):
        try:
            user = TheLanguage.query.filter_by(id=id).first()
            if user:
                user.language = data['language']
                user.framework = data['framework']
                db.session.commit()
                return {'result': 'updated'}, 201
            else:
                return 'Not Available'
        except Exception:
            raise Exception("Issue in updating user information")

    def delete_user_by_id(self, id):
        try:

            user = TheLanguage.query.filter_by(id=id).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                return {'result': 'Deleted'}, 201
            else:
                return 'Not Available'
        except Exception:
            raise Exception("Issue in deleting user")


work = Work()
