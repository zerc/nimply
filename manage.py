# coding: utf-8
from flask.ext.script import Manager

from optimasol import app, base_index

manager = Manager(app)


@manager.command
def grab(filename):
    """
    Read file by `filename` and run develop server with him.
    """
    with open(filename, 'r') as f:
        data = f.read()

    app.view_functions['index'] = lambda *a, **kw: base_index(data, filename)
    app.run()


if __name__ == "__main__":
    manager.run()
