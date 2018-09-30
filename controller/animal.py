from flask import request
from controller.base import BaseController
from model.animal import AnimalModel


class AnimalController(BaseController):

    def __init__(self, app, db):
        super().__init__(app, db)

        self.model = AnimalModel(db)

    def list(self):
        return self.out(self.model.get_all())

    def create(self):
        if not request.is_json:
            return self.out({'error': 'Not JSON request'}, 400)

        data = request.get_json()

        if 'name' not in data:
            return self.out({'error': 'Animal name is empty'}, 400)

        if self.model.is_exists(data['name']):
            return self.out({'error': 'Animal with same name is exists'}, 400)

        animal = self.model.create(data['name'])
        return self.out(animal)
