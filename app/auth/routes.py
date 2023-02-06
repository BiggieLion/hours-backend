from app.utils.validators import validate_user, validate_email_and_password
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, url_for, current_app, request
from app.middlewares.auth import token_required
from datetime import datetime, timedelta
from app.utils.extensions import mongo
from bson.json_util import dumps
from app.models.user import User
from . import auth_router
import traceback
import jwt


@auth_router.route('/', methods=['GET'])  # Test route
@token_required
def test_auth(current_user):
    return {
        'error': False,
        'success': True,
        'message': 'Test from root auth triggered well',
        'data': current_user
    }, 200


@auth_router.route('/signup', methods=['POST'])
def signup_user():
    try:
        user = request.json

        if not user:
            return {
                'error': True,
                'success': False,
                'message': 'Some fields are missing'
            }, 422

        is_user_validated = validate_user(**user)

        if is_user_validated is not True:
            return dict(
                error=True,
                success=False,
                message=is_user_validated
            ), 409

        user = User().create_user(**user)

        if not user:
            return {
                'error': True,
                'success': False,
                'message': 'User already exists'
            }, 409

        return {
            'error': False,
            'success': True,
            'message': 'User created successfully'
        }, 201

    except Exception:
        traceback.print_exc()
        return {
            'error': True,
            'success': False,
            'message': 'Error in server'
        }, 500


@auth_router.route('/signin', methods=['POST'])
def signin_user():
    try:
        data = request.json
        if not data:
            return {
                'error': True,
                'success': False,
                'message': 'Some fields are missing'
            },

        is_email_pass_validated = validate_email_and_password(data.get('email'), data.get('password'))
        if is_email_pass_validated is not True:
            return dict(
                error=True,
                success=False,
                message=is_email_pass_validated
            ), 409

        user = User().signin_user(
            data['email'],
            data['password']
        )

        if user:
            try:
                token_exp_h = current_app.config.get("TOKEN_EXP_H")
                token_exp_m = current_app.config.get("TOKEN_EXP_M")
                user['token'] = jwt.encode(
                    {
                        'user': {
                            '_id': user['_id']
                        }
                    },
                    current_app.config.get("SECRET_KEY"),
                    algorithm='HS256'
                )
                return {
                    'error': False,
                    'success': True,
                    'message': 'User logged successfully',
                    'data': user
                }, 200

            except Exception:
                traceback.print_exc()
                return {
                    'error': True,
                    'success': False,
                    'message': 'Error in server'
                }, 500

        return {
            'error': True,
            'success': False,
            'message': 'Email or password incorrect'
        }, 404

    except Exception:
        traceback.print_exc()
        return {
            'error': True,
            'success': False,
            'message': 'Error in server'
        }, 500
