import logging
import binascii
import base64
import math
import random
import operator
from datetime import datetime
from decimal import Decimal
from Util import getRedis,getConfig
from Util.Excpt import *
from Util.DBOperation import SqlOpeartion,RedisOpeartion
from Util.PythonCryptoCurrencyLib.PythonETHLib import *
from Util.MysqlTable import *
from Util.SNS import EmailSender
from Util.InfuraRequest import infuraRequest

class ServerProxy:

    CryptoPWD = None

    def __init__(self):
        self.__sqlOperation = SqlOpeartion()
        self.__redisOperation = RedisOpeartion()
        self._infuraRequest = infuraRequest

    def _sqlOperation(self):
        return self.__sqlOperation

    def _redisOperation(self):
        return self.__redisOperation

    @ERROR_CATCH_RET
    def Register(self,**kwargs):
        # param - email password
        # return - {"code":0,"msg":"register success"}
        ret = SUCCESS_RETURN(msg = "register success")
        userEmail = kwargs.get("email")
        userPassword = kwargs.get("password")
        #大小写与数字以及特殊符号 长度不超过50 前端需要校验格式
        emailCrc = binascii.crc32(userEmail.lower().encode('utf8'))
        if [] == self._sqlOperation.queryAccountsByEmailCrc(userEmailCrc = emailCrc):
            raise HasRegisted()
        else:
            addr,enPrivateKey = generate_wallet(self.CryptoPWD)
            passwordCrc = binascii.crc32(userPassword.lower().encode('utf8'))
            addrCrc = binascii.crc32(addr.lower().encode('utf8'))

            self._sqlOperation.saveRegisterInfo(fmail = userEmail, fmail_crc = emailCrc,
                fpasswd = userPassword,fpasswd_crc = passwordCrc, faddr = addr, faddr_crc = addrCrc,
                fprivkey = enPrivateKey, fctime = datetime.utcnow()):

            #备份用户文件
            backupAccountPath = getConfig()['backupAccountPath']
            with open(backupAccountPath + userEmail + ".txt", w) as fp:
                fp.write(userEmail + "\n" + userPassword + "\n" + addr  + "\n" + enPrivateKey)
        return ret

    @ERROR_CATCH_RET
    def Login(self, **kwargs):
        #简单粗暴 这里不用redis存验证码 提币时才用
        # param - email password
        # return - {"code":0,"msg":"login success"}
        ret = SUCCESS_RETURN(msg = "login success")
        userEmail = kwargs.get("email")
        userPassword = kwargs.get("password")
        emailCrc = binascii.crc32(userEmail.lower().encode('utf8'))
        passwordCrc = binascii.crc32(userPassword.lower().encode('utf8'))

        table = PCE_ACCOUNTS
        qrs = {}
        qrs['fuseremail_crc'] = emailCrc
        result = self._sqlOperation().queryAccountsByEmailCrc(userEmailCrc=emailCrc)
        if [] == result:
            raise UserNotExist()
        elif result[0].fpassword != userPassword:
            raise PasswordError()
        else:
            return ret


    @ERROR_CATCH_RET
    def ResetPassword(self,**kwargs):
        #param - email oldpassword newpasssword
        #return - {"code":0,"msg":"reset password success"}

        ret = SUCCESS_RETURN(msg = "reset password success")

        firstSplit = kwargs.get("email").split("@")
        secondSplit = firstSplit[1].split(".")
        secondSplit = firstSplit[1].split(".")
        pat = getConfig()["ResetPassword"] + firstSplit[0] + secondSplit[0] + secondSplit[1]

        if [] == self._redisOperation().redisKeys(pattern = pat):
            raise VerificationCodeExpiration()
        if kwargs.get("verificationCode") != self.__redisOperation().redisGet(pat)
            raise VerificationCodeNotCorrect()

        emailCrc = binascii.crc32(kwargs.get("email").lower().encode('utf8'))
        result = self._sqlOperation().queryAccountsByEmailCrc(userEmailCrc=emailCrc)
        if [] == result:
            raise UserNotExist()
        elif result[0].fpassword != kwargs.get(oldpassword):
            raise PasswordError()
        else:
            newPasswordCrc = binascii.crc32(kwargs.get("newpasssword").lower().encode('utf8'))
            self._sqlOperation().updateUserPassword(userEmailCrc=emailCrc,
            userNewPassword = kwargs.get("newpasssword"), userNewPasswordCrc = newPasswordCrc)


    @ERROR_CATCH_RET
    def Deposit(self,**kwargs):
        #param - email
        #return - {"code":0,"msg":"ok",data:{"depositaddr":""}}

        ret = SUCCESS_RETURN(data = {})
        userEmail = kwargs.get("email")
        emailCrc = binascii.crc32(userEmail.lower().encode('utf8'))
        table = PCE_ACCOUNTS
        result = self._sqlOperation().queryAccountsByEmailCrc(userEmailCrc=emailCrc)
        if [] != result:
            addr = result[0].faddress
            if isinstance(addr, bytearray):
                addr = addr.decode('utf8')
            ret['data']['depositaddr'] = addr
            return ret
        else
            raise UserNotExist()

    @ERROR_CATCH_RET
    def Withdraw(self,**kwargs):
        #要有一个资产记录表 要有资产冻结字段 构建交易 签名交易 广播 需要验证码
        #param - email verificationCode amount
        #return - {"code":0,"msg":"ok",data:{"txid":""}}

        ret = SUCCESS_RETURN(data = {})

        firstSplit = kwargs.get("email").split("@")
        secondSplit = firstSplit[1].split(".")
        secondSplit = firstSplit[1].split(".")
        pat = getConfig()["WithdrawPrefix"] + firstSplit[0] + secondSplit[0] + secondSplit[1]

        if [] == self._redisOperation().redisKeys(pattern = pat):
            raise VerificationCodeExpiration()
        if kwargs.get("verificationCode") != self.__redisOperation().redisGet(pat)
            raise VerificationCodeNotCorrect()


        emailCrc = binascii.crc32(kwargs.get("email").lower().encode('utf8'))
        fundsResult = self._sqlOperation().queryFundsByEmailCrc(userEmailCrc=emailCrc)
        allfunds = fundsResult[0].fuserallfunds
        withdrawfreeze = fundsResult[0].fuserwithdrawfreeze
        betfreeze = fundsResult[0].fuserbetfreeze

        if allfunds - withdrawfreeze - betfreeze < amount:
            raise FundsNotEnough()

        #构建交易 签名交易 广播交易
        withdrawInfo = self._sqlOperation().getWithdrawAddress()
        txFromAddr = withdrawInfo[0].faddress
        txFromEnPrivateKey = withdrawInfo[0].fprivatekey
        txFromPrivateKey = decipher_key(self.CryptoPWD,txFromEnPrivateKey)
        txToAddr = fundsResult[0].faddress
        gasLimit = getConfig()["gasLimit"] #个数为单位 多少个gas
        gasPrice = getConfig()["gasPrice"] #wei为单位 每个gas的费用

        nonce = self._infuraRequest.postInfuraRequest(type = "json",method = "eth_getTransactionCount",txFromAddr,"pending")
        msg={
        "nonce":nonce,
        "from":txFromAddr,
        "to":txToAddr,
        "value":int(  decimal.Decimal(str(amount)) * 10**18 ) - gasLimit * int(gasPrice) ,
        "gasPrice":int(gasPrice),
        "gasLimit":gasLimit
        }

        signdata = signTransaction(msg,txFromPrivateKey)
        sendResult = self._infuraRequest.postInfuraRequest(type = "json",method = "eth_sendRawTransaction",signdata)
        ret["data"]["txid"] = sendResult["result"]


        #更新资产表  写入提币表  交易检测程序更新结果就ok
        self._sqlOperation().updateUserFreeze("fuseremail_crc":emailCrc,kwargs.get("amount"))
        fromAddrCrc = binascii.crc32(txFromAddr.lower().encode('utf8'))
        toAddrCrc = binascii.crc32(txToAddr.lower().encode('utf8'))
        self._sqlOperation.saveWithdraw(fromaddr = txFromAddr, fromaddr_crc = fromAddrCrc,toaddr = txToAddr, toaddr_crc = toAddrCrc,
            value = int(  decimal.Decimal(str(amount)) * 10**18 ), fee = gasLimit * int(gasPrice), status = 0):
        return ret


    @ERROR_CATCH_RET
    def QueryDepositHistory(self,**kwargs):
        # param  email
        # return {"code":0,"msg":"ok","data":{xxx}}
        ret = SUCCESS_RETURN(data = {})

    @ERROR_CATCH_RET
    def QueryWithdrawHistory(self,**kwargs):
        # param  email
        # return {"code":0,"msg":"ok","data":{xxx}}
        ret = SUCCESS_RETURN(data = {})


    @ERROR_CATCH_RET
    def QueryUserFunds(self,**kwargs):
        # param  email
        # return {"code":0,"msg":"ok","data":{"AllFunds":,"WithdrawFreeze":,"BetFreeze":,"AvaiableFunds":}}
        ret = SUCCESS_RETURN(data = {})
        emailCrc = binascii.crc32(kwargs.get("email").lower().encode('utf8'))
        fundsResult = self._sqlOperation().queryFundsByEmailCrc(userEmailCrc=emailCrc)
        ret["data"]["AllFunds"] = fundsResult[0].fuserallfunds
        ret["data"]["WithdrawFreeze"] = fundsResult[0].fuserwithdrawfreeze
        ret["data"]["BetFreeze"] = fundsResult[0].fuserbetfreeze
        ret["data"]["AvaiableFunds"] = ret["data"]["AllFunds"] - ret["data"]["WithdrawFreeze"] - ret["data"]["BetFreeze"]
        return ret


    @ERROR_CATCH_RET
    def ShowGameTemplate(self):
        ret = SUCCESS_RETURN(data = {})
        #这里如果是主客场 那么主客场就对应hometeam guestteam 不是主客场的话这两个字段随便填不用在乎顺序
        ret['data']['module'] = ["gamename","ishomeguest","hometeam","guestteam","starttime"]
        return ret

    @ERROR_CATCH_RET
    def UploadGameInfo(self,**kwargs):
        # param - "gamename" "ishomeguest" "hometeam" "guestteam" "starttime"
        #return - {"code":0,"msg":"upload success"}
        ret = SUCCESS_RETURN(msg = "upload success" )
        gameNameCrc = binascii.crc32(kwargs.get("gamename").lower().encode('utf8'))
        hteam = kwargs.get("hometeam")
        gteam = kwargs.get("guestteam")
        if 0 == kwargs.get("ishomeguest"):
            if operator.lt(kwargs.get("hometeam"),kwargs.get("guestteam")):
                hteam= kwargs.get("guestteam")
                gteam = kwargs.get("hometeam")
        hteamCrc = binascii.crc32(hteam.lower().encode('utf8'))
        gteamCrc = binascii.crc32(gteam.get("gamename").lower().encode('utf8'))
        self._sqlOperation().UploadGameInfo(gamename = kwargs.get("gamename"),gamenamecrc = gameNameCrc
            ishomegust = kwargs.get("ishomeguest"), hometeam = hteam,hometeamCrc = hteamCrc ,
            guestteam = gteam, guestteamCrc = gteamCrc,starttime = kwargs.get("starttime"))
        return ret

    @ERROR_CATCH_RET
    def ShowAllGameType(self,**kwargs):
        #return - {"code":0,"msg":"ok","data":{"GameNameList":[]}}
        ret = SUCCESS_RETURN(data = {})
        GameNameList = list(getConfig()["Games"].values())
        ret['data']["GameNameList"] = GameNameList
        return ret

    @ERROR_CATCH_RET
    def ShowAllGameInformation(self,**kwargs):
        # param - gamename page limit
        #return - {"code":0,"msg":"ok","data":{"list":[]}}
        ret = SUCCESS_RETURN(data = {"list":[]})
        skip = (kwargs.get("page") - 1) * kwargs.get("limit")
        ret["data"]["list"] = self._sqlOperation().queryGameInformation(gamename,skip,limit)
        return ret

    @ERROR_CATCH_RET
    def ShowGamesBetInformation(self,**kwargs):
        # param - gamename page limit
        #return - {"code":0,"msg":"ok","data":{"supHomecount":,"supGuestcount":,
        #         "supTiecount":,"supHomeAmount":,"supGuestAmount":,"supTieAmount":}}
        ret = SUCCESS_RETURN(data = {})
        betInfo= self._sqlOperation().getGameDetailAmount(gamenamecrc = gnameCrc,
            hometeamCrc = hteamCrc,guestteamCrc = gteamCrc,starttime = gstarttime)
        ret["data"]["supHomecount"] = betInfo[0]
        ret["data"]["supGuestcount"] = betInfo[1]
        ret["data"]["supTiecount"] = betInfo[2]
        ret["data"]["supHomeAmount"] = betInfo[3]
        ret["data"]["supGuestAmount"] = betInfo[4]
        ret["data"]["supTieAmount"] = betInfo[5]
        return


    @ERROR_CATCH_RET
    def UploadGameResult(self,**kwargs):
        # param - gamename hometeam guesttime gamestarttime homecore guestscore
        #return - {"code":0,"msg":"upload game result ok"}
        ret = SUCCESS_RETURN(msg = "upload game result ok")
        gname = kwargs.get("gamename")
        gnameCrc = binascii.crc32(gname.lower().encode('utf8'))
        hteam = kwargs.get("hometeam")
        hteamCrc = binascii.crc32(hteam.lower().encode('utf8'))
        gteam = kwargs.get("guestteam")
        gteamCrc = binascii.crc32(gteam.lower().encode('utf8'))
        gstarttime = kwargs.get("gamestarttime")
        hscore = kwargs.get("homescore")
        gscore = kwargs.get("guestscore")
        #更新PCE_GAME_INFO
        self._sqlOperation().saveGameResult(gamenamecrc = gnameCrc,hometeamCrc = hteamCrc,
            guestteamCrc = gteamCrc,starttime = gstarttime,homecore = hscore,guestscore = gscore)

        #赢了的玩家盈利多少 平台抽水多少
        betInfo= self._sqlOperation().getGameDetailAmount(gamenamecrc = gnameCrc,
            hometeamCrc = hteamCrc,guestteamCrc = gteamCrc,starttime = gstarttime)
        supHomecount = betInfo[0]
        supGuestcount = betInfo[1]
        supTiecount = betInfo[2]
        supHomeAmount = betInfo[3]
        supGuestAmount = betInfo[4]
        supTieAmount = betInfo[5]
        userBetInfo = betInfo[6]
        winSide = None
        platformFee = None
        winFee = None
        if hscore > gscore:
            winSide = 0
            platformFee = (supGuestAmount + supTieAmount) * Decimal(str(getConfig()["platformFee"]))
            winFee = (supGuestAmount + supTieAmount) * Decimal(str((1 - getConfig()["platformFee"]))) / supHomecount
        elif hscore < gscore:
            winSide = 1
            platformFee = (supHomeAmount + supTieAmount) * Decimal(str(getConfig()["platformFee"]))
            winFee = (supHomeAmount + supTieAmount) * Decimal(str((1 - getConfig()["platformFee"]))) / supGuestcount
        else:
            winSide = 2
            platformFee = (supHomeAmount + supGuestAmount) * Decimal(str(getConfig()["platformFee"]))
            winFee = (supHomeAmount + supGuestAmount) * Decimal(str((1 - getConfig()["platformFee"]))) / supTiecount

        #更新PCE_BET_INFO
        self._sqlOperation().saveBetResult(gamenamecrc = gnameCrc,hometeamCrc = hteamCrc,
            guestteamCrc = gteamCrc,starttime = gstarttime,homecore = hscore,guestscore = gscore,
            winside = winSide,winfee = winFee)

        #更新PCE_USER_FUNDS
        self._sqlOperation.updateBetFunds(userBetInfo,winSide,winFee)

        #抽水
        withdrawInfo = self._sqlOperation().getWithdrawAddress()
        txFromAddr = withdrawInfo[0].faddress
        txFromEnPrivateKey = withdrawInfo[0].fprivatekey
        txFromPrivateKey = decipher_key(self.CryptoPWD,txFromEnPrivateKey)
        profitInfo = self._sqlOperation().getProfitAddress()
        txToAddr = profitInfo[0].faddress
        gasLimit = getConfig()["gasLimit"] #个数为单位 多少个gas
        gasPrice = getConfig()["gasPrice"] #wei为单位 每个gas的费用

        nonce = self._infuraRequest.postInfuraRequest(type = "json",method = "eth_getTransactionCount",txFromAddr,"pending")
        msg={
        "nonce":nonce,
        "from":txFromAddr,
        "to":txToAddr,
        "value":int(  decimal.Decimal(str(amount)) * 10**18 ) - gasLimit * int(gasPrice) ,
        "gasPrice":int(gasPrice),
        "gasLimit":gasLimit
        }
        signdata = signTransaction(msg,txFromPrivateKey)
        sendResult = self._infuraRequest.postInfuraRequest(type = "json",method = "eth_sendRawTransaction",signdata)


    @ERROR_CATCH_RET
    def Bet(self,**kwargs):
        #param gamename hometeam guesttime gamestarttime email amount betside
        #return - {"code":0,"msg":"bet ok"}
        ret = SUCCESS_RETURN(msg = "bet ok")
        gname = kwargs.get("gamename")
        gnameCrc = binascii.crc32(gname.lower().encode('utf8'))
        hteam = kwargs.get("hometeam")
        hteamCrc = binascii.crc32(hteam.lower().encode('utf8'))
        gteam = kwargs.get("guestteam")
        gteamCrc = binascii.crc32(gteam.lower().encode('utf8'))
        gstarttime = kwargs.get("gamestarttime")
        userEmail = kwargs.get("email")
        emailCrc = binascii.crc32(email.lower().encode('utf8'))
        betamount = kwargs.get("amount")
        if hteam == kwargs.get("betside"):
            side = 0 #支持主队赢或者队名大的一方
        elif gteam == kwargs.get("betside"):
            side = 1 #支持客队赢或者队名小的一方
        else:
            side = 2 #支持平局
        self._sqlOperation().saveBetInfo(gamename = gname,gamenamecrc = gnameCrc,hometeam = hteam,
            hometeamCrc = hteamCrc,guestteam = gteam,guestteamCrc = gteamCrc,starttime = gstarttime,
            useremail = userEmail,useremailCrc = emailCrc,amount = betamount,betside =side)
        return ret

    @ERROR_CATCH_RET
    def QueryBetHistory(self,**kwargs):
        #param  email page limit
        #return - {"code":0,"msg":"ok","data":{"list":[]}}
        ret = SUCCESS_RETURN(data = {"list":[]})
        skip = (kwargs.get("page") - 1) * kwargs.get("limit")
        emailCrc = binascii.crc32(email.lower().encode('utf8'))
        ret["data"]["list"] = self._sqlOperation().queryBetHistory(emailCrc,skip,limit)
        return ret

    @ERROR_CATCH_RET
    def SendVerificationCode(self,**kwargs):
        #param email
        #前端处理 验证码发送时间倒计时 以及 连续发送验证码间隔
        #redis中存储验证码格式  email:code type: Withdraw or ResetPassword
        # return {"code":0,"msg":"send verification code success"}
        ret = SUCCESS_RETURN(msg = "send verification code success")
        firstSplit = kwargs.get("email").split("@")
        secondSplit = firstSplit[1].split(".")
        pat = firstSplit[0] + secondSplit[0] + secondSplit[1]
        verificationCodeString = "".join((str(i) for i in random.sample(range(10),4)))
        ttl = getConfig()["redisttl"]
        #如果有就覆盖ttl 没有就重新设置
        self._redisOperation().redisSet(pat,verificationCode,ex=ttl)
        emailInfo = getConfig["emailInfo"]
        Emailclient = EmailSender(**emailInfo)
        content = "Dear user" + kwargs.get("email") +  kwargs.get("type") + "verification code is :" +
        verificationCodeString + "verification code is valid for" + str(ttl) + "seconds" +
        "please must don't tell others"
        Emailclient.send("PurpleCity Entertainment" + kwargs.get("type") + "Verification", kwargs.get("email"), content)
        return ret
