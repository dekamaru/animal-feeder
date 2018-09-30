from model.base import BaseModel


class AnimalScheduleModel(BaseModel):

    def get_by_animal_id(self, animal_id):
        c = self.db.cursor()
        c.execute('SELECT * FROM animal_schedule WHERE animal_id = ?', (animal_id,))
        items = c.fetchall()
        c.close()
        result = []
        if items is not None:
            for item in items:
                result.append(self.transform_schedule_to_object(item))
        return result

    def transform_schedule_to_object(self, db_row):
        return {
            'id': db_row[0],
            'type': db_row[2],
            'time': db_row[3],
            'portions': db_row[4],
            'feed_at': db_row[5]
        }