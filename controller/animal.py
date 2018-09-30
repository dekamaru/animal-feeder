from flask import request
from controller.base import BaseController
from model.animal import AnimalModel
from model.schedule import AnimalScheduleModel
from model.history import AnimalFeedHistory


class AnimalController(BaseController):

    def __init__(self, app, db):
        super().__init__(app, db)

        self.animal_model = AnimalModel(db)
        self.schedule_model = AnimalScheduleModel(db)
        self.feed_history_model = AnimalFeedHistory(db)

    def list(self):
        return self.out(self.animal_model.get_all())

    def view(self, id):
        animal = self.animal_model.get_one_by_id(id)
        if animal is False:
            return self.out({'error': 'Animal not found'}, 404)

        schedule = self.schedule_model.get_by_animal_id(animal['id'])
        history = self.feed_history_model.get_by_animal_id(animal['id'])

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
            return self.out({'error': 'Animal name is empty'}, 400)

        if self.animal_model.is_exists(data['name']):
            return self.out({'error': 'Animal with same name is exists'}, 400)

        animal = self.animal_model.create(data['name'])
        return self.out(animal)
