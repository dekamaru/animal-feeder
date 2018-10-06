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

    def create(self, animal_id, type, time, portions, status):
        sql = 'INSERT INTO feed_history (animal_id, `type`, `time`, portions, status) VALUES (?, ?, ?, ?, ?)'
        c = self.db.cursor()
        c.execute(sql, (animal_id, type, time, portions, status,))
        c.close()

    def transform_history_to_object(self, db_row):
        return {
            'id': db_row[0],
            'animal_id': db_row[1],
            'type': db_row[2],
            'time': db_row[3],
            'portions': db_row[4],
            'status': db_row[5],
            'feed_at': db_row[6]
        }