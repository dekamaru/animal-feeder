from controller.animal import AnimalController
import sqlite3


def load(app):
    db = sqlite3.connect('app.db', check_same_thread=False, isolation_level=None)
    init_db_schema(db)

    animal_controller = AnimalController(app, db)

    app.add_url_rule('/animal', view_func=animal_controller.list, methods={"GET"})
    app.add_url_rule('/animal', view_func=animal_controller.create, methods={"POST"})
    app.add_url_rule('/animal/<id>', view_func=animal_controller.view, methods={"GET"})


    return {'db': db}


def init_db_schema(db):
    c = db.cursor()
    with open('migration.sql', 'r') as migration_file:
        statements = migration_file.read().split(';')

    for stmt in statements:
        c.execute(stmt)

    c.close()
