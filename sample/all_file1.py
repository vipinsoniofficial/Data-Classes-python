from dataclasses import dataclass

import marshmallow_dataclass
from flask import Flask
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///langs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {'lang': 'sqlite:///langs.db'}
app.wsgi_app = ProxyFix(app.wsgi_app)
db = SQLAlchemy(app)

engine1 = db.create_engine('sqlite:///langs.db', {"poolclass": QueuePool, "pool_use_lifo": True})
Session = sessionmaker(bind=engine1)
session1 = Session()


@dataclass
class TheLanguage(db.Model):
    id: int
    language: str
    framework: str

    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(40))
    framework = db.Column(db.String(40))

    def __init__(self, language, framework, **kwargs):
        self.language = language
        self.framework = framework

    def __repr__(self):
        return 'id:{}   {} is the language. {} is the framework.'.format(self.id, self.language, self.framework)


###############################################################################


api = Api(app, version='1.0', title='Data API', description='A simple Data Storing API', )
ns = api.namespace('language', description='CRUD operations')
a_language = api.model('Language', {'language': fields.String("the language."),
                                    'framework': fields.String("The framework")})


class Work:
    @property
    def get_all_user(self):
        users_list = []
        all_users = TheLanguage.query.all()
        # schema = marshmallow_dataclass.class_schema(TheLanguage)
        # for i in all_users:
        #   users_list.append(schema().dump(i))

        schemas = marshmallow_dataclass.class_schema(TheLanguage)
        # print(schemas().dump(all_users, many=True))
        return schemas().dump(all_users, many=True)

    def add_new_user(self, data):
        schema = marshmallow_dataclass.class_schema(TheLanguage)
        new_language = schema().load(data)
        # print("new language:", new_language, type(new_language))

        session1.add(new_language)
        session1.commit()
        return {'result': 'Language added'}, 201

    def get_user_by_id(self, id):
        user = TheLanguage.query.filter_by(id=id).first()
        schema = marshmallow_dataclass.class_schema(TheLanguage)
        result_db = schema().dump(user)
        return result_db

    def update_user_data(self, id, data):
        user = TheLanguage.query.filter_by(id=id).first()
        if user:
            user.language = data['language']
            user.framework = data['framework']
            db.session.commit()
            return {'result': 'updated'}, 201
        else:
            return 'Not Available'

    def delete_user_by_id(self, id):
        user = TheLanguage.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'result': 'Deleted'}, 201
        else:
            return 'Not Available'


work = Work()


@ns.route('/')
class LanguageData(Resource):

    def get(self):
        return work.get_all_user

    @ns.expect(a_language)
    def post(self):
        return work.add_new_user(api.payload)


@ns.route('/<int:id>')
class LanguageModify(Resource):

    def get(self, id):
        return work.get_user_by_id(id)

    @ns.expect(a_language)
    def put(self, id):
        return work.update_user_data(id, api.payload)

    def delete(self, id):
        return work.delete_user_by_id(id)


if __name__ == '__main__':
    db.create_all()
    app.run(port=8991, debug=True)
