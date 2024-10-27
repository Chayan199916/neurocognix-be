from flask import Flask
from .routes.api import api
from .services.use_model import USEModel
from config import Config


def create_app() -> Flask:
    app = Flask(__name__)

    # Initialize USE model
    use_model = USEModel()
    use_model.load_model(Config.MODULE_URL)

    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
