from flask import Flask
from flask_cors import CORS
from .utils.extensions import mongo


def create_app(settings_module='config.development'):
    app = Flask(__name__)
    app.config.from_object(settings_module)

    CORS(
        app, 
        origins='*', 
        methods=['GET', 'POST', 'PUT'], 
        expose_headers=['Authorization', 'Content-Type']
    )

    mongo.init_app(app)

    @app.route('/')
    def test():
        return {
            'message': 'This is a test',
            'test': app.config.get("SECRET_KEY")
        }, 200

    # Importing and registering blueprints
    from .auth import auth_router
    app.register_blueprint(auth_router)

    return app
