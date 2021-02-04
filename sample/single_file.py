from dataclasses import dataclass, field

import marshmallow_dataclass
from flask import Flask
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, Column, String, Integer
from sqlalchemy.orm import sessionmaker, mapper
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

metadata = MetaData()

language_table = Table('language', metadata,
                       Column('id', Integer, primary_key=True, autoincrement=True),
                       Column('language', String(100)),
                       Column('framework', String(100))

)


@dataclass
class TheLanguage:
    id: int = field(default_factory=int)
    # = db.Column(db.Integer, primary_key=True)
    language: str = field(default_factory=str)
    # = db.Column(db.String(40))
    framework: str = field(default_factory=str)
    # = db.Column(db.String(40))

    def __init__(self, id, language, framework):
        self.id = id
        self.language = language
        self.framework = framework

    def __repr__(self):
        return 'id:{}   {} is the language. {} is the framework.'.format(self.id, self.language, self.framework)


mapper(TheLanguage, language_table)


"""
class LanguageSchema(Schema):
    id = mafields.Integer()
    language = mafields.String()
    framework = mafields.String()

    @post_load
    def create_language(self, data, **kwargs):
        return Language(**data)
"""
###############################################################################


api = Api(app, version='1.0', title='Data API', description='A simple Data Storing API',)
ns = api.namespace('language', description='CRUD operations')
a_language = api.model('Language', {'id': fields.Integer("user_id"),
                                    'language': fields.String("the language."),
                                    'framework': fields.String("The framework")})


languages = []
# python = {'language': 'python', 'id': 1}
python = TheLanguage(id=1, language='python', framework='Flask')
checkpoint = True
if not checkpoint:
    languages.append(python)
    db.session.add(python)
    db.session.commit()


class Work:
    @property
    def get_all(self):
        all_users = language_table.query.all()
        schema = marshmallow_dataclass.class_schema(TheLanguage)
        #schema = LanguageSchema(many=True)
        # print(languages)
        return schema().dump(all_users)

    def new(self, data):
        schema = marshmallow_dataclass.class_schema(TheLanguage)
        #schema = LanguageSchema()
        new_language = schema().load(data)
        print(new_language)
        data['id'] = len(TheLanguage.query.all()) + 1
        languages.append(new_language)
        print(languages)

        new_entry = TheLanguage(data['id'], data['language'], data['framework'])
        session1.add(new_entry)
        session1.commit()
        return {'result': 'Language added'}, 201

    def get_id(self, id):
        user = TheLanguage.query.filter_by(id=id).first()
        schema = marshmallow_dataclass.class_schema(TheLanguage)
        #schema = LanguageSchema()
        result_db = schema().dump(user)
        return result_db

    def update(self, id, data):
        user = TheLanguage.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            data['id'] = id
            new_entry = TheLanguage(data['id'], data['language'], data['framework'])
            db.session.add(new_entry)
            db.session.commit()
            return {'result': 'Deleted'}, 201
        else:
            return 'Not Available'

    def delete_id(self, id):
        user = TheLanguage.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'result': 'Deleted'}, 201
        else:
            return 'Not Available'


work = Work()


@ns.route('/')
class Language(Resource):

    def get(self):
        return work.get_all

    @ns.expect(a_language)
    def post(self):
        return work.new(api.payload)


@ns.route('/<int:id>')
class LanguageModify(Resource):
    # @api.marshal_with(a_language, envelope='the_data')
    def get(self, id):
        return work.get_id(id)

    @ns.expect(a_language)
    def put(self, id):
        return work.update(id, api.payload)

    def delete(self, id):
        return work.delete_id(id)


if __name__ == '__main__':
    app.run(port=8991, debug=True)
