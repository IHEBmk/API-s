


# from flask import Blueprint, app, jsonify
from flask import Blueprint, Flask, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from routes.supabasehelper import SupabaseClientSingleton

# from supabasehelper import SupabaseClientSingleton
#app = Flask(__name__)

categories_blueprint = Blueprint('categories', __name__)



@categories_blueprint.route('/GetData', methods=['GET'])
# @jwt_required()
def GetData():
    # user_id=get_jwt_identity()
    supabase=SupabaseClientSingleton()
    # user=supabase.from_('User').select('*').eq('id', user_id)
    # if user:
    response=supabase.from_('Category').select('*').execute()
    print(response.data)
    if response:
            return jsonify({
            "categories": response.data,
     }), 201
    else:
            return jsonify({
            "error": "Error fetching categories"
        }), 400
    
    return jsonify({
            "error": "user not found"
        }), 404

        
@categories_blueprint.route('/GetCategoriesNames', methods=['GET'])
# @jwt_required()
def GetCategoriesNames():
    # user_id=get_jwt_identity()
    supabase=SupabaseClientSingleton()
    # user=supabase.from_('User').select('*').eq('id', user_id)
    # if user:
    
    response=supabase.table('Category').select('id,category').execute()
    
    if response:
            return jsonify({
            "categories": response.data,
     }), 201
    else:
            return jsonify({
            "error": "Error fetching categories"
            
        }), 400
    
    return jsonify({
            "error": "user not found"
        }), 404



