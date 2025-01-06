
from urllib.parse import unquote
from flask import Blueprint, Flask, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from routes.supabasehelper import SupabaseClientSingleton
# app = Flask(__name__)

reciepes_blueprint = Blueprint('recipes', __name__)

@reciepes_blueprint.route('/Get_Dish/<int:id>', methods=['GET'])
# @jwt_required()
def Get_Dish(id):
    # user_id=get_jwt_identity()
    supabase=SupabaseClientSingleton()
    # user=supabase.from_('User').select('*').eq('id', user_id)
    # if user:
    response=supabase.from_('Reciepes').select('*').eq('id', id).limit(1).single().execute()
    
    if response:
            return jsonify({
            "dish": response.data,
     }), 201
    else:
            return jsonify({
            "error": "Error fetching reciepe"
        }), 400
    
    return jsonify({
            "error": "user not found"
        }), 404
        
        
@reciepes_blueprint.route('/Get_Category_Reciepes/<int:categoryId>', methods=['GET'])
# @jwt_required()
def Get_Category_Reciepes(categoryId):
    # user_id=get_jwt_identity()
    supabase=SupabaseClientSingleton()
    # user=supabase.from_('User').select('*').eq('id', user_id)
    # if user:
    response=supabase.from_('Reciepes').select('id,title,subtitle,time,rating,media').eq('category', categoryId).execute()
    
    if response:
            return jsonify({
            "reciepes": response.data,
     }), 201
    else:
            return jsonify({
            "error": "Error fetching reciepes"
        }), 400

    return jsonify({
            "error": "user not found"
        }), 404
        
        
@reciepes_blueprint.route('/Get_Dish_Media/<int:id>', methods=['GET'])
# @jwt_required()
def Get_Dish_Media(id):
    # user_id=get_jwt_identity()
    supabase=SupabaseClientSingleton()
    # user=supabase.from_('User').select('*').eq('id', user_id)
    # if user:
    response=supabase.from_('Media').select('*').eq('id',id).limit(1).single().execute()
    
    if response:
            return jsonify({
            "media": response.data,
     }), 201
    else:
            return jsonify({
            "error": "Error fetching media"
        }), 400

    return jsonify({
            "error": "user not found"        
        }), 404


@reciepes_blueprint.route('/Get_num_reviews/<int:reciepeId>', methods=['GET'])

def Get_num_reviews(reciepeId):
    # user_id=get_jwt_identity()
    supabase=SupabaseClientSingleton()
    # user=supabase.from_('User').select('*').eq('id', user_id)
    # if user:
    response=supabase.from_('Reviews').select('id').eq('reciepe_id', reciepeId).execute()
    
    if response:
            return jsonify({
            "num_reviews": len(response.data),
     }), 201
    else:
            return jsonify({
            "error": "Error fetching num_reviews"
        }), 400

    return jsonify({
            "error": "user not found"
        }), 404
        
        
@reciepes_blueprint.route('/Get_Reciepes_By_Name/<string:name>/<int:limit>', methods=['GET'])
# @jwt_required()
def Get_Reciepes_By_Name(name,limit):
    # user_id=get_jwt_identity()
    supabase=SupabaseClientSingleton()
    # user=supabase.from_('User').select('*').eq('id', user_id)
    # if user:
    name = unquote(name)
    if(limit==1):
            response=supabase.from_('Reciepes').select('id,title').like('title', f'%{name}%').limit(10).execute()
    else:
            response=supabase.from_('Reciepes').select('*').like('title', f'%{name}%').execute()
    
    if response:
            return jsonify({
                    
            "reciepes": response.data,
     }), 201
    else:
            return jsonify({
            "error": "Error fetching reciepes"
        }), 400

    return jsonify({
            "error": "user not found"
        }), 404
        
        
@reciepes_blueprint.route('/Get_Reciepes_By_Exact_ingredients/<string:ingridients>', methods=['GET'])
# @jwt_required()
def Get_Reciepes_By_Exact_ingredients(ingridients):
    # user_id=get_jwt_identity()
    supabase=SupabaseClientSingleton()
    # user=supabase.from_('User').select('*').eq('id', user_id)
    # if user:
    ingridients = unquote(ingridients)
    ingridientts_list=ingridients.split(',')
    ingridientts_list2=[]
    for i in ingridientts_list:
            ingridients_disct={}
            ingridients_disct['ingridient']=i.split('_')[0]
            ingridients_disct['quantity']=i.split('_')[1]
            ingridientts_list2.append(ingridients_disct)
    ingridients_formated=[]
    sorted_list = sorted(ingridientts_list2, key=lambda x: x['ingridient'], reverse=True)
    for i in sorted_list:
            ingridients_formated.append(i['ingridient'])
    ingridients_array = "{" + ",".join(ingridients_formated) + "}"
        
    response=supabase.from_('Reciepes').select('*').eq('ingridients', ingridients_array).execute()
    
    if response:
            return jsonify({
            "reciepes": response.data,
     }), 201
    else:
            return jsonify({
            "error": "Error fetching reciepes"
        }), 400

    return jsonify({
            "error": "user not found"
        }), 404
        
        
@reciepes_blueprint.route('/Get_Reciepes_By_Subset_ingredients/<string:ingridients>', methods=['GET'])
# @jwt_required()
def Get_Reciepes_By_Subset_ingredients(ingridients):
    # user_id=get_jwt_identity()
    supabase=SupabaseClientSingleton()
    # user=supabase.from_('User').select('*').eq('id', user_id)
    # if user:
    
    ingridients = unquote(ingridients)
    ingridientts_list=ingridients.split(',')
    ingridientts_list2=[]
    for i in ingridientts_list:
            ingridients_disct={}
            ingridients_disct['ingridient']=i.split('_')[0]
            ingridients_disct['quantity']=i.split('_')[1]
            ingridientts_list2.append(ingridients_disct)
    ingridients_formated=[]
    
    
    for i in ingridientts_list2:
            ingridients_formated.append(i['ingridient'])
    response=supabase.from_('Reciepes').select('*').contains('ingridients', ingridients_formated).execute()
    
    if response:
            return jsonify({
            "reciepes": response.data,
     }), 201
    else:
            return jsonify({
            "error": "Error fetching reciepes"
        }), 400
    # else:
    return jsonify({
            "error": "user not found"
        }), 404
    
    
@reciepes_blueprint.route('/Get_Reciepes_By_Exact_ingredients_and_quantity/<string:ingridients>', methods=['GET'])
# @jwt_required()
def Get_Reciepes_By_Exact_ingredients_and_quantity(ingridients):
    # user_id=get_jwt_identity()
    supabase=SupabaseClientSingleton()
    # user=supabase.from_('User').select('*').eq('id', user_id)
    # if user:
    
    ingridients = unquote(ingridients)
    print(ingridients)
    ingridientts_list=ingridients.split(',')
    ingridientts_list2=[]
    for i in ingridientts_list:
            ingridients_disct={}
            ingridients_disct['ingridient']=i.split('_')[0]
            ingridients_disct['quantity']=i.split('_')[1]
            ingridientts_list2.append(ingridients_disct)
    ingridients_formated=[]
    quantity_formated=[]
    sorted_list = sorted(ingridientts_list2, key=lambda x: x['ingridient'], reverse=True)
    for i in sorted_list:
            quantity_formated.append(i['quantity'])
            ingridients_formated.append(i['ingridient'])
    print(ingridients_formated)
    print(quantity_formated)
    ingridients_array = "{" + ",".join(ingridients_formated) + "}"
    quantity_array = "{" + ",".join(quantity_formated) + "}"
    response = supabase.from_('Reciepes').select('*')\
        .eq('ingridients', ingridients_array)\
        .eq('quantity', quantity_array)\
        .execute()
    
    if response:
            return jsonify({
            "reciepes": response.data,
     }), 201
    else:
            return jsonify({
            "error": "Error fetching reciepes"
        }), 400

    return jsonify({
            "error": "user not found"
        }), 404