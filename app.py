from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from routes.supabasehelper import SupabaseClientSingleton
from routes.category_api import categories_blueprint
from routes.ingredients_api import ingridients_blueprint
from routes.recipes_api import reciepes_blueprint
from routes.user_api import users_blueprint
from routes.comments_api import comments_blueprint

app = Flask(__name__)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Replace with a secure secret key
app.config['JWT_TOKEN_LOCATION'] = ['headers']

# Initialize JWTManager
jwt = JWTManager(app)





app.register_blueprint(categories_blueprint, url_prefix='/api/categories')
app.register_blueprint(ingridients_blueprint, url_prefix='/api/ingridients')
app.register_blueprint(reciepes_blueprint, url_prefix='/api/recipes')
app.register_blueprint(users_blueprint, url_prefix='/api/users')
app.register_blueprint(comments_blueprint, url_prefix='/api/comments')




if __name__ == "__main__":
    app.run(debug=True)
