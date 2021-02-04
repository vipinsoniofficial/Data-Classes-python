from config import db
from dataclasses import dataclass


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

