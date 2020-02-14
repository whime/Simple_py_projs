'''
models,corresponing to tables in database,
table_name is what the model_name is,temporarily.
'''

from python_orm_test.Fields import *
import asyncio
from python_orm_test.sqlOperation import *


def create_args_string(num):
    L=[]
    for _ in range(num):
        L.append('?')
    return ','.join(L)
# 创建where子句
def make_where_statement(keys):
    s=''
    num=len(keys)
    for _ in range(num):
        s+='%s=? and '
    return s[:-5]
# 定义model类的元类
class ModelMetaclass(type):
    def __new__(cls,name,bases,attrs):
        if name=="Model":
            return type.__new__(cls,name,bases,attrs)

        # 获取表的名称,或无提供__table__参数则使用name参数
        tableName=getattr(cls,'__table__',None) or name
        mappings={}
        fields=[]
        primaryKey=None
        for key,value in attrs.items():
            if isinstance(value,Field):
                mappings[key]=value
                if value.primary_key:
                    if primaryKey:
                        raise RuntimeError('Duplicate primary key for table %s'%tableName)
                    primaryKey=key
                else:
                    fields.append(key)
        # TODO(whime): 自动生成id作为primary key备份
        if not primaryKey:
            raise RuntimeError('primary key not found!!')
        for key in mappings.keys():
            attrs.pop(key)
        escaped_fields=list(map(lambda f:str(f),fields))
        attrs['__mappings__']=mappings
        attrs['__table__']=tableName
        attrs['__primary_key__']=primaryKey
        attrs['__fields__']=fields #没有包含主键名

        attrs['__select__'] = 'select %s, %s from %s' % (primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into %s (%s, %s) values (%s)' % (
        tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update %s set %s where %s=?' % (
        tableName, ', '.join(map(lambda f: '%s=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from %s where %s=?' % (tableName, primaryKey)

        return type.__new__(cls,name,bases,attrs)

# 编写基类model,继承自内置类dict
class Model(dict,metaclass=ModelMetaclass):

    @classmethod
    async def get(cls,orderby=None,limit=None,**kw):
        'get objects by where statement'
        keys=kw.keys()
        values=list(kw.values())

        args=[]
        if orderby is not None:
            args.append('order by')
            args.append(orderby)
        if limit is not None:
            args.append('limit')
            if isinstance(limit,int):
                args.append(str(limit))
            elif isinstance(limit,tuple):
                args.append(str(limit))
            else:
                raise ValueError('Invalid limit value:%s'%str(limit))

        sql=('%s where '+make_where_statement(keys))%(cls.__select__,*keys)+' '.join(args)
        rs=await select (sql,values)
        if len(rs)==0:
            return None
        return [cls(**r) for r in rs]

    @classmethod
    async def filter(cls):
        # TODO(whime):
        pass

    def __init__(self,**kw):
        super().__init__(**kw)

    def __getattr__(self,key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("'Model' object has no attribute '%s'"%key)
    def __setattr__(self,key,value):
        self[key]=value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    async def save(self):
        # 执行字段验证
        from copy import deepcopy
        fields=deepcopy(self.__fields__)
        fields.append(self.__primary_key__) #添加主键一起验证

        for field in fields:
            fieldObj=self.__mappings__[field]
            value=self.getValueOrDefault(field)

            if not fieldObj.validate(value):
                raise Exception("Field %s expects %s type,%s found"%(field,fieldObj.column_type,type(value)))

        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))

        rows = await execute(self.__insert__, args)
        if rows != 1:
            logging.warn('failed to insert record: affected rows: %s' % rows)

    async def update(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))

        rows = await execute(self.__update__, args)
        if rows != 1:
            logging.warn('failed to update by primary key: affected rows: %s' % rows)

    async def delete(self):
        args=self.getValueOrDefault(self.__primary_key__)
        rows=await execute(self.__delete__,args)

        if rows != 1:
            logging.warn('failed to delete by primary key: affected rows: %s' % rows)


