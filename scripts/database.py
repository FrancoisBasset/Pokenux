#!/usr/bin/env python
import os
import sqlite3

pokenux_path: str = os.path.expanduser('~') + '/.pokenux'
database_path: str = pokenux_path + '/pokenux.db'

def create_personal_folder():
    if not os.path.exists(os.path.expanduser('~') + '/.pokenux'):
        os.mkdir(os.path.expanduser('~') + '/.pokenux')

def create_database():
    common_database = sqlite3.connect(database_path)
    common_database.execute('CREATE TABLE settings (id TEXT PRIMARY KEY, name TEXT, logo TEXT, release_date TEXT)')

create_personal_folder()
create_database()