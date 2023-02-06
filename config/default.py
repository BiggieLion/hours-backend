import os
from dotenv import load_dotenv
from os.path import abspath, dirname, join

load_dotenv()

# Setting the application directory
BASE_DIR = dirname(dirname(abspath(__file__)))

# Setting the default variables
SECRET_KEY = os.getenv('SECRET_KEY')
TOKEN_KEY = os.getenv('TOKEN_KEY')