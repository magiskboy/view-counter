# coding=utf-8
import os
import json
import pymysql
from pymysql import cursors
from tasks import q, on_viewed



def index(environ):
    q.enqueue(on_viewed, environ['PATH_INFO'])
    return 'Lmao', 200, [('Content-Type', 'plain/text')]


def stat(environ):
    db = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'viewcounter'),
        password=os.getenv('DB_PASS', 'pass'),
        port=os.getenv('DB_PORT', 3306),
        db=os.getenv('DB_NAME', 'viewcounter'),
        cursorclass=cursors.DictCursor
    )
    try:
        url = '/'
        with db.cursor() as cur:
            sql = r'select n from stat where url = %s'
            cur.execute(sql, (url,))
            r = cur.fetchone()
    except:
        return 'Internal server error', 500, {}
    else:
        return json.dumps(r), 200, [('Content-Type', 'application/json')]
    finally:
        db.close()


routers = {
    '/': index,
    '/stat': stat,
}


def default_handler():
    return 'Not Found', 404, {}


def wsgi(environ, start_response):
    path = environ['PATH_INFO']
    handler = routers.get(path, default_handler)
    content, status, headers = handler(environ)
    start_response(str(status), headers)
    return [content.encode('utf-8')]
