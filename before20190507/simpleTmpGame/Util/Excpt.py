import logging
import json
import traceback

class PCE_Exception(Exception):

    ERROR_CODE = None
    ERROR_MSG = None

    def __init__(self, *args, **kwargs):
        if args:
            self.MSG = args
        elif kwargs:
            self.MSG = kwargs
        else:
            self.MSG = None

    def __int__(self):
        return self.ERROR_CODE

    def __str__(self):
        msg = self.ERROR_MSG
        if self.MSG:
            if msg is None:
                msg = '{}'.format(MSG)
            else:
                msg += ' : {}'.format(MSG)
        return msg


class SqlDatabaseError(PCE_Exception):
    """sql数据库异常"""
    ERROR_CODE = 1001
    ERROR_MSG = 'sql database error'

class RedisError(PCE_Exception):
    """redis异常"""
    ERROR_CODE = 1002
    ERROR_MSG = 'redis error'

class InnerUrlConfigError(PCE_Exception):
    """内部接口配置异常"""
    ERROR_CODE = 1003
    ERROR_MSG = 'inner url config error'

class InnerServerNotFindUrlMethodError(PCE_Exception):
    """BackendServer没有找到对应url的处理方法"""
    ERROR_CODE = 1004
    ERROR_MSG = 'inner server not find relevant method with url'


class HasRegisted(PCE_Exception):
    ERROR_CODE = 1005
    ERROR_MSG = "this email has registed"

class UserNotExist(PCE_Exception):
    ERROR_CODE = 1006
    ERROR_MSG = "User not exist"

class PasswordError(PCE_Exception):
    ERROR_CODE = 1007
    ERROR_MSG = "password error"

class EmailSendError(PCE_Exception):
    ERROR_CODE = 1008
    ERROR_MSG = "email send error"

class VerificationCodeExpiration(PCE_Exception):
    ERROR_CODE = 1009
    ERROR_MSG = "verification code expiration"

class VerificationCodeNotCorrect(PCE_Exception):
    ERROR_CODE = 1010
    ERROR_MSG = "verification code not correct"

class FundsNotEnough(PCE_Exception):
    ERROR_CODE = 1011
    ERROR_MSG = "funds not enough"


class SUCCESS_RETURN(UserDict):

    def __init__(self, msg = "ok", **kwargs):
        UserDict.__init__(self, code = 0, msg = str(msg), **kwargs)

class ERROR_RETURN(UserDict):

    def __init__(self, code = -1, msg = "unknown error":
        UserDict.__init__(self, code = int(code), msg = str(msg))

'''
{"code":0,"msg"="ok"},{"code":0,"msg"="ok","data":{}}
{"code":self.ERROR_CODE,"msg"="self.ERROR_MSG + self.MSG"}
'''

def ERROR_CATCH_RAISE(function):
    def inner(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as err:
            traceback.print_exc()
            raise err
    return inner

def ERROR_CATCH_RET(function):
    def inner(*args, **kwargs):
        try:
            ret = function(*args, **kwargs)
        except Exception as err:
            traceback.print_exc()
            if isinstance(err,PCE_Exception):
                ret = ERROR_RETURN(code = int(err), msg = str(err)
            else:
                ret = ERROR_RETURN()
        finally:
            return ret
    return inner

def ERROR_CATCH_PASS(function):
    def inner(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as err:
            traceback.print_exc()
    return inner
