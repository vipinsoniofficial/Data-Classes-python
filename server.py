from config import app,api
from controllers.user_controller import ns as user_ns

api.add_namespace(user_ns)


if __name__ == '__main__':
    app.run(port=9999, debug=True)