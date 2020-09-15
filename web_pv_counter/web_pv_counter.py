#!/usr/bin/python3
import cgi
import cgitb

cgitb.enable(display=1, logdir='/tmp')

import datetime
import os
from peewee import * # install with root



pg_db = PostgresqlDatabase('blogdb', user='blog', password='blog',
    host='127.0.0.1', port=5432)

class BaseModel(Model):
    class Meta:
        database = pg_db

class Message(BaseModel):
    url = CharField()
    addr = CharField()
    time = DateTimeField()

def create_tables():
    with pg_db:
        pg_db.create_tables([Message])

def show_env_params():
    for param in os.environ.keys():
        print("<b>%20s</b>: %s</br>" % (param, os.environ[param]))

def get_page_view(url=None):
    if url is None:
        return 0
    return len(Message.select().where(Message.url == url))

def add_page_view(url=None, addr=None):
    if url is None:
        return 0
    Message.create(url=url, addr=addr, time=datetime.datetime.now())
    return len(Message.select().where(Message.url == url))


if __name__ == '__main__':
    form = cgi.FieldStorage()
    print('Content-Type: text/plain\n')
    # show_env_params()
    url = form.getfirst("url", None)
    addr = os.environ['REMOTE_ADDR']
    if os.environ['REQUEST_METHOD'] == 'GET':
        pv = get_page_view(url)
    else:
        pv = add_page_view(url, addr)
    print(pv)
