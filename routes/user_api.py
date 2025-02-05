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