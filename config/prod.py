import os
from .default import *

MONGO_URI = os.getenv('MONGO_LOCAL')
TOKEN_EXP_H = 24
TOKEN_EXP_M = 0