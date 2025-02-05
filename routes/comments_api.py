from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from routes.supabasehelper import SupabaseClientSingleton
from datetime import datetime 
# Create a Blueprint for comment-related routes
comments_blueprint = Blueprint('comments', __name__)

@comments_blueprint.route('/comments', methods=['POST'])
@jwt_required()
def insert_comment():
    data = request.get_json()
    if not data or 'recipe_id' not in data or 'comment' not in data or 'rating' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    # Get the current user's email from the JWT token
    current_user_email = get_jwt_identity()

    # Fetch the username associated with the email
    supabase = SupabaseClientSingleton()
    user_response = supabase.from_('user').select('username').eq('email', current_user_email).single().execute()

    if not user_response.data:
        return jsonify({"error": "User not found"}), 404

    username = user_response.data['username']

    # Insert the comment with the username
    comment_response = supabase.from_('comments').insert({
        'recipe_id': data['recipe_id'],
        'username': username,  # Use the fetched username
        'comment': data['comment'],
        'rating': data['rating'],
        'date': datetime.utcnow().isoformat() 
    }).execute()

    if comment_response:
        return jsonify({"message": "Comment inserted successfully"}), 201
    else:
        return jsonify({"error": "Error inserting comment"}), 400

# Get all comments for a specific recipe
@comments_blueprint.route('/comments/recipe/<string:recipe_id>', methods=['GET'])
def get_recipe_comments(recipe_id):
    supabase = SupabaseClientSingleton()
    response = supabase.from_('comments').select('*').eq('recipe_id', recipe_id).order('date', desc=True).execute()
    if response:
        return jsonify({"comments": response.data}), 200
    else:
        return jsonify({"error": "Error fetching comments"}), 400

# Get average rating for a recipe
@comments_blueprint.route('/comments/recipe/<string:recipe_id>/average_rating', methods=['GET'])
def get_recipe_average_rating(recipe_id):
    supabase = SupabaseClientSingleton()
    response = supabase.from_('comments').select('rating').eq('recipe_id', recipe_id).execute()
    if not response.data:
        return jsonify({"average_rating": 0.0}), 200

    ratings = [float(comment['rating']) for comment in response.data]
    average_rating = sum(ratings) / len(ratings) if ratings else 0.0
    return jsonify({"average_rating": average_rating}), 200


# Get comment count for a recipe
@comments_blueprint.route('/comments/recipe/<string:recipe_id>/count', methods=['GET'])
def get_recipe_comment_count(recipe_id):
    supabase = SupabaseClientSingleton()
    response = supabase.from_('comments').select('id').eq('recipe_id', recipe_id).execute()
    if response:
        return jsonify({"comment_count": len(response.data)}), 200
    else:
        return jsonify({"error": "Error fetching comment count"}), 400


# Update a comment
@comments_blueprint.route('/comments/<int:id>', methods=['PUT'])
@jwt_required()
def update_comment(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Ensure the user updating the comment is the one who created it
    current_user_email = get_jwt_identity()
    supabase = SupabaseClientSingleton()

    # Fetch the comment to check ownership
    comment_response = supabase.from_('comments').select('user_email').eq('id', id).single().execute()
    if not comment_response.data or comment_response.data['user_email'] != current_user_email:
        return jsonify({"error": "Unauthorized to update this comment"}), 403

    response = supabase.from_('comments').update(data).eq('id', id).execute()
    if response:
        return jsonify({"message": "Comment updated successfully"}), 200
    else:
        return jsonify({"error": "Error updating comment"}), 400


# Delete a comment
@comments_blueprint.route('/comments/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_comment(id):
    # Ensure the user deleting the comment is the one who created it
    current_user_email = get_jwt_identity()
    supabase = SupabaseClientSingleton()

    # Fetch the comment to check ownership
    comment_response = supabase.from_('comments').select('user_email').eq('id', id).single().execute()
    if not comment_response.data or comment_response.data['user_email'] != current_user_email:
        return jsonify({"error": "Unauthorized to delete this comment"}), 403

    response = supabase.from_('comments').delete().eq('id', id).execute()
    if response:
        return jsonify({"message": "Comment deleted successfully"}), 200
    else:
        return jsonify({"error": "Error deleting comment"}), 400


# Get user's comments
@comments_blueprint.route('/comments/user', methods=['GET'])
@jwt_required()
def get_user_comments():
    # Get the current user's email from the JWT token
    # Get the current user's email from the JWT token
    current_user_email = get_jwt_identity()

    # Fetch the username associated with the email
    supabase = SupabaseClientSingleton()
    user_response = supabase.from_('user').select('username').eq('email', current_user_email).single().execute()

    if not user_response.data:
        return jsonify({"error": "User not found"}), 404

    username = user_response.data['username']

    response = supabase.from_('comments').select('*').eq('username', username).order('date', desc=True).execute()
    if response:
        return jsonify({"comments": response.data}), 200
    else:
        return jsonify({"error": "Error fetching user comments"}), 400


# Check if user has already commented on a recipe
@comments_blueprint.route('/comments/has_commented', methods=['GET'])
@jwt_required()
def has_user_commented():
    recipe_id = request.args.get('recipe_id')
    if not recipe_id:
        return jsonify({"error": "recipe_id is required"}), 400

    # Get the current user's email from the JWT token
    current_user_email = get_jwt_identity()

    supabase = SupabaseClientSingleton()
    response = supabase.from_('comments').select('id').eq('user_email', current_user_email).eq('recipe_id', recipe_id).execute()
    if response:
        return jsonify({"has_commented": len(response.data) > 0}), 200
    else:
        return jsonify({"error": "Error checking if user has commented"}), 400