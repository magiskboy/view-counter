# coding=utf-8

import os
import pymysql
from pymysql import cursors
import rq
import redis


q = rq.Queue(connection=redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=os.getenv('REDIS_PORT', 6379),
    db=0,
))

cache = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=os.getenv('REDIS_PORT', 6379),
    db=1,
)


def on_viewed(url):
    cache.incr(url, 1)


def update_counter():
    try:
        db = pymysql.connect(
            os.getenv('DB_HOST', 'localhost'),
            os.getenv('DB_USER', 'viewcounter'),
            os.getenv('DB_PASS', 'pass'),
            os.getenv('DB_PORT', 3306),
            os.getenv('DB_NAME', 'viewcounter'),
            cursorclass=cursors.DictCursor
        )
        for url in cache.keys():
            c = cache.get(url)
            with db.cursor() as cur:
                cur.execute('select * from stat where url = %s', (url,))
                n = cur.fetchone()
                if n[0] == 0:
                    cur.execute('insert into stat(url, n) values (%s, %s)', (url, c))
                else:
                    cur.execute('update stat set n = %s where url = %s', (c, url))
        db.commit()
    except:
        db.rollback()
    finally:
        db.close()
