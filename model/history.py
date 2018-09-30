from model.base import BaseModel


class AnimalFeedHistory(BaseModel):

    def get_by_animal_id(self, animal_id):
        c = self.db.cursor()
        c.execute('SELECT * FROM feed_history WHERE animal_id = ?', (animal_id,))
        items = c.fetchall()
        c.close()
        result = []
        if items is not None:
            for item in items:
                result.append(self.transform_history_to_object(item))
        return result

    def transform_history_to_object(self, db_row):
        return {
            'id': db_row[0],
            'time': db_row[2],
            'portions': db_row[3]
        }