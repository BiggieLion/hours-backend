from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.extensions import mongo
from datetime import datetime
from bson import ObjectId

userColl = mongo.db.users


class User:
    """ User Model """
    def __init__(self):
        return

    def create_user(self, username = '', email = '', password = ''):
        """ Method to create a new user """
        user = self.get_by_email(email)
        if user:
            return
        new_user = userColl.insert_one({
            'username': username,
            'email': email,
            'password': self.encrypt_password(password),
            'status': 1,
            'rol': 1,
            'created_at': datetime.today().replace(microsecond=0),
            'updated_at': datetime.today().replace(microsecond=0),
        })
        return self.get_by_id(new_user.inserted_id)

    def get_all(self):
        """ Method to get all the auth """
        users = userColl.find()
        return [{**users, '_id': str(user['_id'])} for user in users]

    def get_by_id(self, user_id):
        """ Method to get a user by its id """
        user = userColl.find_one({ '_id': ObjectId(user_id) })

        if not user:
            return

        user['_id'] = str(user['_id'])
        user.pop('password')
        return user

    def get_by_email(self, email):
        """ Method to get a user by its email """
        user = userColl.find_one({ 'email': email })
        if not user:
            return
        user['_id'] = str(user['_id'])
        return user

    def update_username(self, user_id, data):
        """ Update the username for a user """
        user = userColl.update_one(
            {
                '_id': ObjectId(user_id)
            },
            {
                '$set': data
            }
        )
        user = self.get_by_id(user_id)
        return user

    def delete_user(self, user_id):
        """ Method to delete a user """
        user = userColl.delete_one({ '_id': ObjectId(user_id) })
        user = self.get_by_id(user_id)
        return user

    def disable_account(self, user_id):
        user = userColl.update_one(
            {
                '_id': ObjectId(user_id)
            },
            {
                '$set': {
                    'status': 0
                }
            }
        )
        user = self.get_by_id(user_id)
        return user

    def signin_user(self, email, password):
        """ Method to a user can login """
        user = self.get_by_email(email)
        if not user or not check_password_hash(user['password'], password):
            return
        user.pop("password")
        return user

    def encrypt_password(self, password):
        """ Method to encrypt the user password """
        return generate_password_hash(password)
