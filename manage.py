# coding: utf-8
from flask.ext.script import Manager

from app import app

manager = Manager(app)


@manager.command
def grab(filename):
    """
    Read file by `filename` and run develop server with him.
    """
    from nimply import base_index

    with open(filename, 'r') as f:
        data = f.read()

    app.view_functions['index'] = lambda *a, **kw: base_index(data, filename)
    app.run()


@manager.command
def runserver():
    # app.run()
    app.run(host='0.0.0.0', port=8000)


if __name__ == "__main__":
    manager.run()
