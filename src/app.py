"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


jackson_family = FamilyStructure("Jackson")


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def members_list():
    
    try:    
        members = jackson_family.get_all_members()

        if not members:
            return jsonify({"error": "No members found"}), 400
        
        response_body = {
            "family": members
        }

        return jsonify(response_body), 200
    
    except Exception as e:

        return jsonify({
            "error": "An error occurred while retrieving members.",
            "message": str(e)
        }), 500

@app.route('/members/<int:id>', methods=['GET'])
def get_memberById(id):
    try:
        
        member = jackson_family.get_member(id)

        
        if not member:
            return jsonify({"error": f"Member with ID {id} not found"}), 404

       
        response_body = {
            "id": member["id"],
            "first_name": member["first_name"],
            "age": member["age"],
            "lucky_numbers": member["lucky_numbers"]
        }
        return jsonify(response_body), 200

    except Exception as e:
        
        return jsonify({
            "error": "An error occurred while retrieving the member.",
            "message": str(e)
        }), 500

@app.route('/members', methods=['POST'])
def add_member():
    try:
        
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body is missing"}), 400

        
        required_fields = ["first_name", "age", "lucky_numbers"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"'{field}' is required"}), 400

      
        member = jackson_family.add_member({
            "first_name": data["first_name"],
            "age": data["age"],
            "lucky_numbers": data["lucky_numbers"]
        })

        
        response_body = {
            "id": member["id"],
            "first_name": member["first_name"],
            "age": member["age"],
            "lucky_numbers": member["lucky_numbers"]
        }

        return jsonify(response_body), 201

    except Exception as e:
        return jsonify({
            "error": "An error occurred while adding the member.",
            "message": str(e)
        }), 500
    
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        
        member = jackson_family.delete_member(id)

        if not member:
            return jsonify({"error": f"Member with ID {id} not found"}), 404

        
        response_body = {
            "message": f"Member with ID {id} has been successfully deleted"
        }
        return jsonify(response_body), 200

    except Exception as e:
        
        return jsonify({
            "error": "An error occurred while deleting the member.",
            "message": str(e)
        }), 500




if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
