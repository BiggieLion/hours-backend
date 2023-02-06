from flask import redirect, url_for, current_app, request
from app.utils.extensions import mongo
from bson.json_util import dumps
from . import auth_router

@auth_router.route('/', methods=['GET']) # Test route
def test_auth():
    return {
        'message': 'FROM AUTH BLUE'
    }, 200

@auth_router.route('/signup', methods=['POST'])
def signup_user():
    print(request.json)
    return {
        'message': 'world hold on'
    }, 200
