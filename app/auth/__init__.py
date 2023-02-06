from flask import Blueprint

auth_router = Blueprint('auth', __name__, url_prefix='/auth')

from . import routes