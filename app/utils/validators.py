""" Validators module """
from bson import ObjectId
import re


def validate(data, regexp):
    """ Custom validator """
    return True if re.match(regexp, data) else False


def validate_password(password: str):
    """
        Validates if the password has the following characteristics:
        - Is more than 8 characters but less than 20
        - Contains at least an uppercase and lowercase letters
        - Contains at least a number
        - Contains at least one or more of the following special chars: @$!%*#?&
    """
    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
    return validate(password, reg)


def validate_email(email: str):
    """ Validate if the email check all the standard email characteristics """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return validate(email, regex)


def validate_email_and_password(email, password):
    """ Easy function to validate both email and password """
    if not (email and password):
        return {
            'email': 'Missing',
            'password': 'Missing'
        }
    if not validate_email(email):
        return {
            'email': 'Invalid'
        }
    if not validate_password(password):
        return {
            'password': 'Invalid'
        }
    return True


def validate_user(**args):
    """ User validator """
    if not args.get('email') or not args.get('password') or not args.get('username'): # Verifying if all the necessary fields to create a user exists
        return {
            'username': 'Missing',
            'email': 'Missing',
            'password': 'Missing'
        }
    if not isinstance(args.get('username'), str) or not isinstance(args.get('email'), str) or not isinstance(args.get('password'), str): # Verifying if all the fields are strings
        return {
            'username': 'Not a String',
            'email': 'Not a String',
            'password': 'Not a String'
        }
    if not validate_email(args.get('email')):
        return {
            'email': 'Invalid'
        }
    if not validate_password(args.get('password')):
        return {
            'password': 'Invalid'
        }
    if not 2 <= len(args['username'].split(' ')) <= 30:
        return {
            'username': 'Invalid (more than 2 but less than 30)'
        }
    return True