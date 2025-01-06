from flask import Flask,app
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from routes.supabasehelper import SupabaseClientSingleton
from routes.category_api import categories_blueprint
from routes.ingredients_api import ingridients_blueprint
from routes.recipes_api import reciepes_blueprint
app = Flask(__name__)

bcrypt=None
# jwt = JWTManager(app)





app.register_blueprint(categories_blueprint, url_prefix='/api/categories')
app.register_blueprint(ingridients_blueprint, url_prefix='/api/ingridients')
app.register_blueprint(reciepes_blueprint, url_prefix='/api/recipes')




# def create_app():
#     app = Flask(__name__)

    
#     return app


# @app.route('/')
# def hello_world():
#     return 'Hello, World!'


if __name__ == "__main__":
    app.run(debug=True)
