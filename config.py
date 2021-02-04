from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_restx import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///langs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {'lang': 'sqlite:///langs.db'}
app.wsgi_app = ProxyFix(app.wsgi_app)
db = SQLAlchemy(app)

engine1 = db.create_engine('sqlite:///langs.db', {"poolclass": QueuePool, "pool_use_lifo": True})
Session = sessionmaker(bind=engine1)
session1 = Session()

api = Api(app, version='1.0', title='Data API', description='A simple Data Storing API', )