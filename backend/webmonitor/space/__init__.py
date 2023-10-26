from flask import Blueprint

space_bp = Blueprint('space', __name__)

from webmonitor.space import view