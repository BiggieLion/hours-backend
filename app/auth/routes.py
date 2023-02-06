from flask import redirect, url_for, current_app, request
from app.utils.extensions import mongo
from bson.json_util import dumps
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import auth_router
import traceback


@auth_router.route('/', methods=['GET']) # Test route
def test_auth():
    return {
        'message': 'FROM AUTH BLUE'
    }, 200

@auth_router.route('/signup', methods=['POST'])
def signup_user():
    try:
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        verifier = mongo.db.users.find_one({ 'email': email })
        if verifier is not None:
            return {
                'error': True,
                'success': False,
                'message': 'This user already exists'
            }, 409
        if username and email and password:
            hasshed_pass = generate_password_hash(password, "sha256")
            user = {
                'username': username,
                'email': email,
                'password': hasshed_pass,
                'created_at': datetime.today().replace(microsecond=0),
                'updated_at': datetime.today().replace(microsecond=0),
            }
            inserted = mongo.db.users.insert_one(user)
            if inserted is not None:
                return {
                    'error': False,
                    'success': True,
                    'message': 'The user has been succesfully registered'
                }, 201
            else:
                return {
                'error': True,
                'success': False,
                'message': 'Error on creating'
            }, 500
        else: 
            return {
                'error': True,
                'success': False,
                'message': 'Some fields are missing'
            }, 422
    except Exception:
        traceback.print_exc()
        return {
            'error': True,
            'success': False,
            'message': 'Error in server'
        }, 500

