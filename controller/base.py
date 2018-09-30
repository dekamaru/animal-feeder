from flask import make_response
import json


class BaseController(object):

    def __init__(self, app, db):
        self.app = app
        self.db = db

    def out(self, content, code=200, is_json=True):
        if is_json:
            content = json.dumps(content)
        response = make_response(content, code)
        response.headers['Content-Type'] = 'application/json'
        return response
