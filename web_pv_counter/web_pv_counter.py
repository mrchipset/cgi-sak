#!/usr/bin/python3
import cgi
import cgitb
import datetime
import os
# from peewee import *

cgitb.enable(display=0, logdir='/tmp')


pg_db = PostgresqlDatabase('testdb', user='user', password='passwd',
    host='127.0.0.1', port=5432)

class BaseModel(Model):
    class Meta:
        database = pg_db

class Messsage(BaseModel):
    url = CharField()
    addr = CharField()
    time = DateTimeField()

def create_tables():
    with pg_db:
        pg_db.create_tables([Messsage])

def show_env_params():
    for param in os.environ.keys():
        print("<b>%20s</b>: %s</br>" % (param, os.environ[param]))


def add_page_view(url=None, addr=None):
    if url is None:
        return 0
    Messsage.create(url=url, addr=addr, time=datetime.datetime.now())
    return len(Messsage.select().where(Messsage.url == url))


if __name__ == '__main__':
    form = cgi.FieldStorage()
    print('Content-Type: text/plain\n')
    # show_env_params()
    url = form.getfirst("url", None)
    addr = os.environ['REMOTE_ADDR']
    pv = add_page_view(url, addr)
    print(pv)
