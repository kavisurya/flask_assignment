from flask import Flask,Blueprint ,request, jsonify
from api_controller.user_endpoints import userAPI_routes
from flask_cors import CORS


def create_app():
    web_app = Flask(__name__)

    CORS(web_app)

    api_blueprint = Blueprint('api_blueprint', __name__)
    api_blueprint = userAPI_routes(api_blueprint)

    web_app.register_blueprint(api_blueprint, url_prefix="/api/v1/")

    return web_app


app = create_app()

if __name__ == "__main__":
    app.run(debug=False, port="5000")