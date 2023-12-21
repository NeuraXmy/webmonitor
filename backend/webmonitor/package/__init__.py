from flask import Blueprint

package_bp = Blueprint('package', __name__)

from webmonitor.package import view