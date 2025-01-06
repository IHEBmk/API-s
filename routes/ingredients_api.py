


from flask import Blueprint, Flask, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from routes.supabasehelper import SupabaseClientSingleton
ingridients_blueprint = Blueprint('ingridients', __name__)
#app = Flask(__name__)

@ingridients_blueprint.route('/Search_Ingridients/<string:name>', methods=['GET'])
# @jwt_required()
def Search_Ingridients(name):
    # user_id=get_jwt_identity()
    supabase=SupabaseClientSingleton()
    # user=supabase.from_('User').select('*').eq('id', user_id)
    # if user:
    response=supabase.from_('Ingridients').select('*').like('ingridient', f'%{name}%').execute()
    
    if response:
            return jsonify({
                
            "ingridients": response.data,
     }), 201
    else:
            return jsonify({
            "error": "Error fetching ingridients"
        }), 400
    
    return jsonify({
            "error": "user not found"
        }), 404