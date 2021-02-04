from flask_restx import Resource, fields
from config import api
from services.user_services import work


ns = api.namespace('language', description='CRUD operations')
a_language = api.model('Language', {'language': fields.String("the language."),
                                    'framework': fields.String("The framework")})


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
