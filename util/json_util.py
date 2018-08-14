# coding:utf-8
import json
from datetime import datetime
from uuid import UUID


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, UUID):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def json_dump(result):
    return json.dumps(result, cls=CJsonEncoder)
