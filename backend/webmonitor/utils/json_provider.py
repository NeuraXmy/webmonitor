from flask import current_app
from datetime import datetime
from flask.json.provider import DefaultJSONProvider
from webmonitor.utils.page import PaginationData

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):

        if isinstance(obj, datetime):
            time_format = current_app.config.get('TIME_FORMAT')
            return obj.strftime(time_format)
        
        if isinstance(obj, PaginationData):
            return {
                'total': obj.total,
                'page': obj.page,
                'size': obj.size,
                'pages': obj.pages,
                'items': obj.items,
            }

        return super().default(obj)