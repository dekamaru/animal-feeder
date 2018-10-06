from model.base import BaseModel


class AnimalScheduleModel(BaseModel):

    def get_by_animal_id(self, animal_id):
        c = self.db.cursor()
        c.execute('SELECT * FROM animal_schedule WHERE animal_id = ? ORDER BY time ASC', (animal_id,))
        items = c.fetchall()
        c.close()
        result = []
        if items is not None:
            for item in items:
                result.append(self.transform_schedule_to_object(item))
        return result

    def get_by_time(self, time):
        c = self.db.cursor()
        c.execute('SELECT * FROM animal_schedule WHERE `time` = ?', (time,))
        item = c.fetchone()
        print(item)
        c.close()
        if item is not None:
            item = self.transform_schedule_to_object(item)
        return item

    def update(self, animal_id, schedule):
        create_sql = 'INSERT INTO animal_schedule (animal_id, time, portions) VALUES (?, ?, ?)'
        update_sql = 'UPDATE animal_schedule SET time = ?, portions = ? WHERE id = ?'
        c = self.db.cursor()
        for item in schedule:
            if item['id'] == '':
                c.execute(create_sql, (animal_id, item['time'], item['portions']))
            else:
                c.execute(update_sql, (item['time'], item['portions'], item['id']))
        c.close()

    def remove(self, schedule_id):
        c = self.db.cursor()
        c.execute('DELETE FROM animal_schedule WHERE id = ?', (schedule_id,))
        c.close()

    def transform_schedule_to_object(self, db_row):
        return {
            'id': db_row[0],
            'animal_id': db_row[1],
            'time': db_row[2],
            'portions': db_row[3]
        }