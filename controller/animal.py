from flask import request
from controller.base import BaseController
from model.animal import AnimalModel
from model.schedule import AnimalScheduleModel
from model.history import AnimalFeedHistory


class AnimalController(BaseController):

    def __init__(self, app, db):
        super().__init__(app, db)

        self.am = AnimalModel(db)
        self.asm = AnimalScheduleModel(db)
        self.afh = AnimalFeedHistory(db)

    def list(self):
        return self.out(self.am.get_all())

    def view(self, id):
        animal = self.am.get_one_by_id(id)
        if animal is False:
            return self.out({'error': 'Animal not found'}, 404)

        schedule = self.asm.get_by_animal_id(animal['id'])
        history = self.afh.get_by_animal_id(animal['id'])

        return self.out({
            'info': animal,
            'schedule': schedule,
            'history': history
        })

    def create(self):
        if not request.is_json:
            return self.out({'error': 'Not JSON request'}, 400)

        data = request.get_json()

        if 'name' not in data:
            return self.out({'error': 'Animal name is empty'}, 402)

        if self.am.is_exists(data['name']):
            return self.out({'error': 'Animal with same name is exists'}, 402)

        animal = self.am.create(data['name'])
        return self.out(animal)
