# coding: utf-8
from flask.ext.script import Manager

from app import app

manager = Manager(app)


@manager.command
def runserver():
    app.run(host='0.0.0.0', port=8000)


if __name__ == "__main__":
    manager.run()
