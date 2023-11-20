from flask import current_app
from datetime import datetime
from flask.json.provider import DefaultJSONProvider

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, datetime):
            time_format = current_app.config.get('TIME_FORMAT')
            return obj.strftime(time_format)
        return super().default(obj)