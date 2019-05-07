from Util.Excpt import (ERROR_CATCH_RAISE, RedisError)
from Util import getRedis

class RedisOpeartion:

    def __init__(self):
        self.__redisInstance = getRedis()

    @ERROR_CATCH_RAISE
    def redisHgetAll(self,Hname): #是一个dict
        try:
            ret = self.__redisInstance.hgetall(Hname)
            return ret
        except Exception as err:
            traceback.print_exc()
            logging.error("redisHgetAll redis failed!")
            raise RedisError()

    @ERROR_CATCH_RAISE
    def redisGet(self,name): #是一个dict
        try:
            ret = self.__redisInstance.get(name)
            return ret
        except Exception as err:
            traceback.print_exc()
            logging.error("redisHgetAll redis failed!")
            raise RedisError()

    @ERROR_CATCH_RAISE
    def redisKeys(self, pattern = '*'): #是一个list
        try:
            ret = self.__redisInstance.keys(pattern = pattern)
            return ret
        except Exception as err:
            traceback.print_exc()
            logging.warning("redisKeys redis failed!")
            raise RedisError()

    @ERROR_CATCH_RAISE
    def redisSet(self, name, value, ex=None, px=None, nx=False, xx=False):
        try:
            ret = self.__redisInsance.set(name, value, ex, px, nx, xx)
            return ret
        except Exception as err:
            traceback.print_exc()
            logging.error("redisSet redis failed!")
            raise RedisError()
    
