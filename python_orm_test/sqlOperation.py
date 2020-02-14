'''
somw function to execute sql statement using aiomysql
'''
import aiomysql
import asyncio
import logging

@asyncio.coroutine
def create_pool(**kw):
    logging.info('create database connection pool...')
    global __pool
    __pool=yield from aiomysql.create_pool(
        host=kw.get('host','127.0.0.1'),
        port=kw.get('port',3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        autocommit=kw.get('autocommit',True)
    )

@asyncio.coroutine
def select(sql,args,size=None):
    global __pool
    with (yield from __pool) as conn:
        cur=yield from conn.cursor(aiomysql.DictCursor)
        yield from cur.execute(sql.replace('?','%s'),args or ())
        if size:
            rs=yield from cur.fetchmany(size)
        else:
            rs=yield from cur.fetchall()
        yield from cur.close()
        logging.info('rows return:%s'%len(rs))
        return rs

async def execute(sql, args, autocommit=True):

    async with __pool.acquire() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                print(sql.replace('?', '%s'), args)
                await cur.execute(sql.replace('?', '%s'), args)
                affected = cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected