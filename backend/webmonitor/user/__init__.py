from flask import Blueprint

user_bp = Blueprint('user', __name__)

from webmonitor.user import view