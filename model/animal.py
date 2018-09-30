class AnimalModel(object):

    def __init__(self, db):
        self.db = db

    def create(self, name):
        c = self.db.cursor()
        c.execute('INSERT INTO animal (name) VALUES (?)', (name,))
        c.close()
        return self.get_one_by_name(name)

    def get_one_by_name(self, name):
        c = self.db.cursor()
        c.execute('SELECT * FROM animal WHERE name = ?', (name,))
        item = c.fetchone()
        c.close()
        return self.transform_animal_to_object(item)

    def get_all(self):
        c = self.db.cursor()
        c.execute('SELECT * FROM animal')
        items = c.fetchall()
        c.close()
        result = []
        for item in items:
            result.append(self.transform_animal_to_object(item))
        return result

    def is_exists(self, name):
        c = self.db.cursor()
        c.execute('SELECT count(*) FROM animal WHERE name = ?', (name,))
        count = c.fetchone()[0]
        c.close()
        return count != 0

    def transform_animal_to_object(self, db_result):
        return {
            'id': db_result[0],
            'name': db_result[1]
        }
