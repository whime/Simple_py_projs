from python_orm_test.db.models import Model
from python_orm_test.Fields import *
from python_orm_test.sqlOperation import *
import asyncio
# TODO(WHIME):需要手动创建表
class person(Model):
    id=IntegerField(primary_key=True)
    name=StringField()
    length=FloatField()

async def test():
    await create_pool(user='root',password='root',db='orm')
    u=person(id=9,name='Anny',length=18.2333)
    print(u)
    await u.save()

if __name__=='__main__':
    loop=asyncio.get_event_loop()
    loop.run_until_complete(test())
    print("done")