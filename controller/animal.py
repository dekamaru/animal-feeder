from flask import request
from controller.base import BaseController
from model.animal import AnimalModel
from model.schedule import AnimalScheduleModel
from model.history import AnimalFeedHistory
from feeder.feeder_factory import AbstractFeederFactory
import datetime


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

    def update_schedule(self, id):
        if not request.is_json:
            return self.out({'error': 'Not JSON request'}, 400)

        data = request.get_json()

        self.schedule_model.update(id, data)

        return self.out({'status': True})

    def delete_schedule(self, id):
        self.schedule_model.remove(id)
        return self.out({'status': True})

    def scheduled_feed(self):
        now = datetime.datetime.now()
        time = "%s:%s" % (str(now.hour).zfill(2), str(now.minute).zfill(2))
        schedule = self.schedule_model.get_by_time(time)
        if schedule is not None:
            try:
                feeder = AbstractFeederFactory().create()
            except ImportError:
                self.feed_history_model.create(
                    schedule['animal_id'],
                    'AUTO',
                    time,
                    schedule['portions'],
                    'BACKEND_FAILED'
                )
                return self.out({
                    'error': 'Backend has import error'
                }, 500)

            feeder.feed(schedule['portions'])

            self.feed_history_model.create(
                schedule['animal_id'],
                'AUTO',
                time,
                schedule['portions'],
                'OK'
            )

        return self.out({
            'status': True
        })


