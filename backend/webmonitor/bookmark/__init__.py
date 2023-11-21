from flask import Blueprint

bookmark_bp = Blueprint('bookmark', __name__)

from webmonitor.bookmark import view