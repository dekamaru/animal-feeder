from flask import send_file, send_from_directory

from controller.base import BaseController


class IndexController(BaseController):

    def index(self):
        return send_file('frontend/index.html')

    def static_files(self, path):
        return send_from_directory('frontend/assets', path)

