from flask import Blueprint

watch_bp = Blueprint('watch', __name__)

from webmonitor.watch import view