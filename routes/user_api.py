from flask import Blueprint, jsonify, request
from routes.supabasehelper import SupabaseClientSingleton
from flask_jwt_extended import create_access_token

# Create a Blueprint for user-related routes
users_blueprint = Blueprint('users', __name__)

# Get all users
@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    supabase = SupabaseClientSingleton()
    response = supabase.from_('user').select('id, username, phone, email, birthdate').execute()
    if response:
        return jsonify({"users": response.data}), 200
    else:
        return jsonify({"error": "Error fetching users"}), 400

# Insert a new user
@users_blueprint.route('/users/insert', methods=['POST'])
def insert_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    supabase = SupabaseClientSingleton()
    response = supabase.from_('user').insert(data).execute()
    if response:
        return jsonify({"message": "User inserted successfully"}), 201
    else:
        return jsonify({"error": "Error inserting user"}), 400

# Update an existing user
@users_blueprint.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    supabase = SupabaseClientSingleton()
    response = supabase.from_('user').update(data).eq('id', id).execute()
    if response:
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"error": "Error updating user"}), 400

# Delete a user
@users_blueprint.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    supabase = SupabaseClientSingleton()
    response = supabase.from_('user').delete().eq('id', id).execute()
    if response:
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"error": "Error deleting user"}), 400

# Get user by ID
@users_blueprint.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    supabase = SupabaseClientSingleton()
    response = supabase.from_('user').select('id, username, phone, email, birthdate').eq('id', id).single().execute()
    if response:
        return jsonify({"user": response.data}), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Get user by email
@users_blueprint.route('/users/email/<string:email>', methods=['GET'])
def get_user_by_email(email):
    supabase = SupabaseClientSingleton()
    response = supabase.from_('user').select('id, username, phone, email, birthdate').eq('email', email).single().execute()
    if response:
        return jsonify({"user": response.data}), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Authenticate user
@users_blueprint.route('/users/authenticate', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password are required"}), 400

    supabase = SupabaseClientSingleton()
    response = supabase.from_('user').select('id, username, phone, email, birthdate').eq('email', data['email']).eq('password', data['password']).maybe_single().execute()
    
    if response.data:
        # Generate a JWT token
        access_token = create_access_token(identity=data['email'])
        return jsonify({
            "user": response.data,
            "access_token": access_token
        }), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

# Update user password
@users_blueprint.route('/users/update_password', methods=['PUT'])
def update_password():
    data = request.get_json()
    if not data or 'email' not in data or 'new_password' not in data:
        return jsonify({"error": "Email and new password are required"}), 400

    supabase = SupabaseClientSingleton()
    response = supabase.from_('user').update({'password': data['new_password']}).eq('email', data['email']).execute()
    if response:
        return jsonify({"message": "Password updated successfully"}), 200
    else:
        return jsonify({"error": "Error updating password"}), 400

# Get current logged-in user
@users_blueprint.route('/users/current', methods=['GET'])
def get_current_user():
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({"error": "Email is required"}), 400

    supabase = SupabaseClientSingleton()
    response = supabase.from_('user').select('id, username, phone, email, birthdate').eq('email', data['email']).single().execute()
    if response:
        return jsonify({"user": response.data}), 200
    else:
        return jsonify({"error": "User not found"}), 404
    
    
    
@users_blueprint.route('/users/get_favourites/<int:user_id>', methods=['GET'])
def get_Favourites(user_id):
    supabase = SupabaseClientSingleton()
    response = supabase.from_('Favourites').select('id,reciepe_id').eq('user_id', user_id).execute()
    if response:
        return jsonify({"favourites": response.data}), 200
    else:
        return jsonify({"error": "User not found"}), 404





@users_blueprint.route('/users/remove_favourites/<int:id>', methods=['GET'])
def remove_Favourites(id):
    supabase = SupabaseClientSingleton()
    response = supabase.from_('Favourites').delete().eq('id', id).execute()
    if response:

        return jsonify({"message": "Favourite removed successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404
    
    
    
    
@users_blueprint.route('/users/add_favourites/<int:user_id>/<int:id>', methods=['GET'])
def add_Favourites(user_id,id):
    supabase = SupabaseClientSingleton()
    response = supabase.from_('Favourites').insert({'user_id': user_id, 'reciepe_id': id}).execute()
    if response:
        return jsonify({"message": "Favourite added successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404





@users_blueprint.route('/update/<int:user_id>', methods=['PUT'])
def update_user_info(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    supabase = SupabaseClientSingleton()
    fields_to_update = {}
    allowed_fields = ["full_name", "bio", "username"] 

    # Update allowed text fields
    for field in allowed_fields:
        if field in data and isinstance(data[field], str):
            fields_to_update[field] = data[field]

    # Handle profile image upload
    if "profile_img" in data and data["profile_img"]:
        try:
            # Validate Base64 string length before decoding
            if len(data["profile_img"]) % 4 != 0:
                return jsonify({"error": "Invalid base64 image data"}), 400

            image_data = base64.b64decode(data["profile_img"])
            image_filename = f"profile_images/{uuid.uuid4()}.jpg"

            storage_response = supabase.storage.from_('ProfileImages').upload(image_filename, image_data, {
                "content-type": "image/jpeg"
            })

            # Check for storage upload errors
            if isinstance(storage_response, dict) and "error" in storage_response:
                return jsonify({"error": f"Error uploading image: {storage_response['error']}"}), 500

            image_url = supabase.storage.from_('ProfileImages').get_public_url(image_filename)
            fields_to_update["profile_img"] = image_url
        except Exception as e:
            return jsonify({"error": f"Image processing error: {str(e)}"}), 500

    if not fields_to_update:
        return jsonify({"error": "No valid fields to update"}), 400

    try:
        response = supabase.from_('user').update(fields_to_update).eq('id', user_id).execute()

        if not response:
            return jsonify({"error": "Error updating user", "details": response["error"]}), 400

        return jsonify({"message": "User updated successfully", "updated_data": fields_to_update}), 200
    except Exception as e:
        return jsonify({"error": f"Database update error: {str(e)}"}), 500
    
    

@users_blueprint.route('/user_favorites/<user_id>', methods=['GET'])
def get_user_favorites(user_id):
    try:
        supabase = SupabaseClientSingleton()

        # Get favorite recipe IDs for the user
        fav_response = supabase.from_("Favourites").select("reciepe_id").eq("user_id", user_id).execute()

        if hasattr(fav_response, 'error') and fav_response.error:
            return jsonify({
                "error": "Database error",
                "details": fav_response.error
            }), 400

        favorite_recipe_ids = [fav["reciepe_id"] for fav in fav_response.data]

        if not favorite_recipe_ids:
            return jsonify({
                "message": "No favorite recipes found for this user",
                "recipes": []
            }), 200

        # Get details of the favorite recipes
        recipes_response = supabase.from_("Reciepes").select("*").in_("id", favorite_recipe_ids).execute()

        if hasattr(recipes_response, 'error') and recipes_response.error:
            return jsonify({
                "error": "Database error",
                "details": recipes_response.error
            }), 400

        return jsonify({
            "message": "Favorite recipes retrieved successfully",
            "length": len(recipes_response.data),
            "recipes": recipes_response.data
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Failed to retrieve favorite recipes",
            "details": str(e),
            "type": type(e).__name__
        }), 500
        
@users_blueprint.route('getme/<int:id>', methods=['GET'])
def get_user(id):
    supabase = SupabaseClientSingleton()
    response = supabase.from_('user').select('*').eq('id', id).execute()

    if response.data:
        return jsonify({"user": response.data}), 200
    else:
        return jsonify({"error": f"User not found with ID {id}"}), 404