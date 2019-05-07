import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Util.Except import SqlDatabaseError

class MysqlEngine:
    def __init__(self, user, password, host, dbname, pool_size = 3, pool_recycle = 60):
        prefix = 'mysql+mysqlconnector://'
        address = '{0}:{1}@{2}/{3}'.format(user, password, host, dbname)
        option = '?auth_plugin=mysql_native_password'
        self.__url =  prefix + address + option
        self.__engine = create_engine(self.__url, pool_size = pool_size,
                pool_recycle = pool_recycle, echo = False)
        self.__session = sessionmaker(bind = self.__engine)

    def session(self):
        return self.__session()

    def query(self, table, close = True, **kwargs):
        try:
            session = self.session()
            result = session.query(table)
            if {} != kwargs:
                result = result.filter_by(**kwargs)
            result = result.all()
            if False == close:
                return (session, result)
            else:
                return (None, result)
        except Exception as err:
            close = True
            logging.error('query exception: {}'.format(err))
            raise SqlDatabaseError()
        finally:
            if True == close:
                session.close()

    def insert(self, records, commit = True):
        try:
            ret = None
            session = self.session()
            session.add_all(records)
            if True == commit:
                session.commit()
            else:
                ret = session
            return ret
        except Exception as err:
            session.rollback()
            commit = True
            logging.error('insert exception: {}'.format(err))
            raise SqlDatabaseError()
        finally:
            if True == commit:
                session.close()

    def update(self, table, conds, commit = True, **kwargs):
        # conds 过滤条件，是一个字典。
        try:
            ret = None
            session = self.session()
            records = session.query(table).filter_by(**conds).all()
            for record in records:
                setattr(record, key, value) for key, value in kwargs.items()]
            if True == commit:
                session.commit()
            else:
                ret = session
            return ret
        except Exception as err:
            session.rollback()
            commit = True
            logging.error('update exception: {}'.format(error))
            raise SqlDatabaseError()
        finally:
            if True == commit:
                session.close()

    def execute(self, sql):
        pass
