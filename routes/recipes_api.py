
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
    ingridientts_list2=ingridients.split(',')

    sorted_list = sorted(ingridientts_list2,reverse=True)

    ingridients_array = "{" + ",".join(sorted_list) + "}"
        
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
    ingridientts_list2=ingridients.split(',')
    
    ingridients_formated=[]
    
    

    response=supabase.from_('Reciepes').select('*').contains('ingridients', ingridientts_list2).execute()
    
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
    
    
    


@reciepes_blueprint.route('/add_recipe', methods=['POST'])
def add_recipe():
    data = request.get_json()

    required_fields = ["category", "title", "details", "steps", "ingridients", "nutritional_val", "time", "rating", "user_id", "subtitle", "quantity"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    supabase = SupabaseClientSingleton()
    media_id = None 

    if "video" in data or "images" in data:
        media_data = {"video": None, "images": []}

        if "video" in data and data["video"]:
            try:
                video_data = base64.b64decode(data["video"])
                video_filename = f"{uuid.uuid4()}.mp4"

                storage_response = supabase.storage.from_("videos").upload(video_filename, video_data, {"content-type": "video/mp4"})
                
                if hasattr(storage_response, 'error') and storage_response.error:
                    return jsonify({"error": f"Error uploading video: {storage_response.error}"}), 500

                media_data["video"] = supabase.storage.from_("videos").get_public_url(video_filename)
            except Exception as e:
                return jsonify({
                    "error": "Video processing error",
                    "details": str(e),
                    "type": type(e).__name__
                }), 500

        if "images" in data and isinstance(data["images"], list):
            for img_base64 in data["images"][:2]:  # Max 2 images
                try:
                    image_data = base64.b64decode(img_base64)
                    image_filename = f"reciepes/{uuid.uuid4()}.jpg"

                    storage_response = supabase.storage.from_("Images").upload(image_filename, image_data, {"content-type": "image/jpeg"})
                    
                    if hasattr(storage_response, 'error') and storage_response.error:
                        return jsonify({"error": f"Error uploading image: {storage_response.error}"}), 500

                    media_data["images"].append(supabase.storage.from_("Images").get_public_url(image_filename))
                except Exception as e:
                    return jsonify({
                        "error": "Image processing error",
                        "details": str(e),
                        "type": type(e).__name__
                    }), 500

        try:
            media_response = supabase.from_("Media").insert([{
                "video": media_data["video"],
                "images": media_data["images"]
            }]).execute()

            if not media_response.data or len(media_response.data) == 0:
                return jsonify({
                    "error": "Error inserting media",
                    "response": media_response.__dict__
                }), 400

            media_id = media_response.data[0]["id"]
        except Exception as e:
            return jsonify({
                "error": "Media insertion error",
                "details": str(e),
                "type": type(e).__name__,
                "args": getattr(e, 'args', []),
                "response": getattr(e, 'response', None)
            }), 500

    try:
        recipe_data = {
            "category": data["category"],
            "media": media_id, 
            "title": data["title"],
            "details": data["details"],
            "steps": data["steps"],  
            "ingridients": data["ingridients"],  
            "nutritional_val": data["nutritional_val"], 
            "time": data["time"],
            "rating": data["rating"],
            "user_id": data["user_id"],
            "subtitle": data["subtitle"],
            "quantity": data["quantity"] 
        }
        
        print("Formatted data for database:", recipe_data)  
        
        try:
            
            recipe_response = supabase.from_("Reciepes").insert([recipe_data]).execute()
            print("Supabase response:", recipe_response) 
            
            if hasattr(recipe_response, 'error') and recipe_response.error:
                return jsonify({
                    "error": "Database error",
                    "details": recipe_response.error,
                    "data": recipe_data
                }), 400

            if not recipe_response.data or len(recipe_response.data) == 0:
                return jsonify({
                    "error": "No data returned",
                    "response": recipe_response.__dict__,
                    "data": recipe_data
                }), 400

            return jsonify({
                "message": "Recipe added successfully",
                "recipe_id": recipe_response.data[0]["id"],
                "data": recipe_data
            }), 201
            
        except Exception as db_error:
            print("Database error:", str(db_error))  
            return jsonify({
                "error": "Database operation failed",
                "details": str(db_error),
                "type": type(db_error).__name__,
                "data": recipe_data
            }), 500
            
    except Exception as e:
        print("General error:", str(e)) 
        return jsonify({
            "error": "Recipe insertion error",
            "details": str(e),
            "type": type(e).__name__,
            "args": getattr(e, 'args', []),
            "response": getattr(e, 'response', None)
        }), 500
        
        
@reciepes_blueprint.route('/user_recipes/<user_id>', methods=['GET'])
def get_user_recipes(user_id):
    try:
        supabase = SupabaseClientSingleton()
        
        # Fetch user recipes along with media details
        response = (
            supabase.from_("Reciepes")
            .select("*, Media(id, images)")
            .eq("user_id", user_id)
            .execute()
        )

        if hasattr(response, 'error') and response.error:
            return jsonify({
                "error": "Database error",
                "details": response.error
            }), 400

        if not response.data or len(response.data) == 0:
            return jsonify({
                "message": "No recipes found for this user",
                "recipes": []
            }), 200

        recipes = response.data

        # Extract first image from the "images" field
        for recipe in recipes:
            if "Media" in recipe and recipe["Media"]:
                try:
                    images = json.loads(recipe["Media"]["images"])  # Convert string to JSON
                    if isinstance(images, list) and len(images) > 0:
                        recipe["image"] = images[0]  # First image
                    else:
                        recipe["image"] = None
                except Exception:
                    recipe["image"] = None
            else:
                recipe["image"] = None

        return jsonify({
            "message": "Recipes retrieved successfully",
            "length": len(recipes),
            "recipes": recipes
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Failed to retrieve recipes",
            "details": str(e),
            "type": type(e).__name__
        }), 500