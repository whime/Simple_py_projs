'''
数据库表的字段名和字段类型
'''

class Field():
    def __init__(self,name,column_type,primary_key,default):
        self.name=name
        self.column_type=column_type
        self.primary_key=primary_key
        self.default=default
    def __str__(self):
        return '<%s,%s,%s>'%(self.__class__.__name__,self.column_type,self.name)


class StringField(Field):
    def __init__(self,name=None,primary_key=False,default=None,max_length=20):
        super().__init__(name,"varchar",primary_key=False,default=None)
        self.max_length=max_length

    def validate(self,value):
        if value is not None:
            if isinstance(value,str) and len(value)<self.max_length:
                return True
            else:return False
        else:
            return True


class IntegerField(Field):
    def __init__(self,name=None,primary_key=False,default=None):
        super().__init__(name,"int",primary_key,default)

    def validate(self,value):
        if value is not None:
            return isinstance(value,int)
        return True

class FloatField(Field):
    '''
    :param bound: num of the digits after decimal point
    '''
    def __init__(self,name=None,primary_key=False,default=None):
        super().__init__(name,"float",primary_key,default)

    def validate(self,value):
        if value is not None:
            return isinstance(value,float)
        return True