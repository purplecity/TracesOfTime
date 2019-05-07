import os
import json
import logging

global _sqlengine
global _config_path

_sqlengine = None
_config_path = None

__all__ = ['getRedis','getSqlengine', 'getSqlSession', 'getConfig']

def getRedis():
    import redis
    config = getConfig()
    redisconfig = config['redis']
    redisInstance= redis.StrictRedis(**redisconfig)
    return redisInstance

def getSqlengine():
    from Util.MysqlEngine import MysqlEngine
    global _sqlengine
    if _sqlengine is None:
        config = getConfig()
        mysql = config['mysql']
        _sqlengine = MysqlEngine(**mysql)
    return _sqlengine

def getSqlSession():
    from Util.MysqlEngine import MysqlEngine
    global _sqlengine
    if _sqlengine is None:
        config = getConfig()
        mysql = config['mysql']
        _sqlengine = MysqlEngine(**mysql)
    return _sqlengine.session()


def getConfig():
    global _config_path
    if _config_path is None:
        _config_path = os.path.dirname(os.path.realpath(__file__))
        _config_path +=  '/config.json'
    cfile = _config_path
    with open(cfile, 'r', encoding='utf8') as fs:
        config = json.load(fs)
        fs.close()
        return config
