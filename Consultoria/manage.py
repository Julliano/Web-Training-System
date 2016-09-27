#!env/bin/python
# coding: utf-8
from flask_migrate import MigrateCommand
from flask_script import Manager
from consultoria import create_app

manager = Manager(create_app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()