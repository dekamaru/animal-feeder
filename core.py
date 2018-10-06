from controller.animal import AnimalController
from controller.index import IndexController
import sqlite3

def load(app):
    db = sqlite3.connect('app.db', check_same_thread=False, isolation_level=None)
    init_db_schema(db)

    index_controller = IndexController(app, db)
    animal_controller = AnimalController(app, db)

    # frontend
    app.add_url_rule('/', view_func=index_controller.index, methods={"GET"})
    app.add_url_rule('/assets/<path:path>', view_func=index_controller.static_files, methods={"GET"})

    # backend
    app.add_url_rule('/animal', view_func=animal_controller.list, methods={"GET"})
    app.add_url_rule('/animal', view_func=animal_controller.create, methods={"POST"})
    app.add_url_rule('/animal/<id>', view_func=animal_controller.view, methods={"GET"})

    # schedule
    app.add_url_rule('/schedule/<id>', view_func=animal_controller.delete_schedule, methods={"DELETE"})
    app.add_url_rule('/animal/<id>/schedule', view_func=animal_controller.update_schedule, methods={"PUT"})
    app.add_url_rule('/schedule/feed', view_func=animal_controller.scheduled_feed, methods={"GET"})

    return {'db': db}


def init_db_schema(db):
    c = db.cursor()
    with open('migration.sql', 'r') as migration_file:
        statements = migration_file.read().split(';')

    for stmt in statements:
        c.execute(stmt)

    c.close()
