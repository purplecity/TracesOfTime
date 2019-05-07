from Util import getSqlengine
from Util.MysqlTable import *
from Util.Excpt import ERROR_CATCH_RAISE,SqlDatabaseError
from datatime import datetime
from decimal import Decimal

class SqlOpeartion:

    def __init__(self):
        self.__sqlengine = getSqlengine()

    def _sqlengine(self):
        return self.__sqlengine

    @ERROR_CATCH_RAISE
    def queryAccountsByEmailCrc(self,amount,userEmailCrc = None):
        table = PCE_ACCOUNTS
        qrs = {}
        qrs['fuseremail_crc'] = userEmailCrc
        _, result = self._sqlengine().query(table, **qrs)
        return result


    @ERROR_CATCH_RAISE
    def updateUserFreeze(self, userEmailCrc = None, amount):
        table = PCE_USER_FUNDS
        qrs = {}
        qrs['fuseremail_crc'] = userEmailCrc
        session, result = self._sqlengine().query(table, commit = False, **qrs)
        freeze =result[0].fuserwithdrawfreeze
        try:
            result[0].fuserwithdrawfreeze = freeze + amount
            session.commit()
        except Exception as err:
            session.rollback()
            logging.error("update freeze error")
            raise SqlDatabaseError()
        finally:
            session.close()

    @ERROR_CATCH_RAISE
    def saveRegisterInfo(self,fmail = '', fmail_crc = 0, fpasswd = '',
            fpasswd_crc = 0, faddr = '', faddr_crc = 0, fprivkey = '', fctime = datetime.utcnow()):
        table = PCE_ACCOUNTS
        record = table(fuseremail = fmail, fuseremail_crc = fmail_crc, fpassword = fpasswd,fpassword_crc = fpasswd_crc,
            faddress = faddr, faddress_crc = faddr_crc,fprivatekey = fprivkey, fcreatetime = fctime)
        self._sqlengine().insert([record])

    @ERROR_CATCH_RAISE
    def getWithdrawAddress(self,type = 0):
        table = PCE_BOOS_INFO
        qrs = {}
        qrs["ftype"] = type
        qrs["valid"] = 1
        _,result = self._sqlengine().query(table,**qrs)
        return result

    def getProfitAddress(self,type = 0):
        table = PCE_BOOS_INFO
        qrs = {}
        qrs["ftype"] = type
        qrs["valid"] = 1
        _,result = self._sqlengine().query(table,**qrs)
        return result


    @ERROR_CATCH_RAISE
    def saveWithdraw(self,height = 0,txid = "", txid_crc = "", fromaddr = "", fromaddr_crc = "",
            toaddr = "", toaddr_crc = "", value = 0, fee = 0, status = 0, createtime = datetime.utcnow(),
            finishtime = datetime.utcnow()):
        table = PCE_WITHDRAW
        record = table(fheight = height, ftxid = txid, ftxid_crc = txid_crc,ffromaddr = fromaddr,
            ffromaddr_crc = fromaddr_crc, toaddr = faddr_crc,ftoaddr_crc = toaddr_crc, fvalue = value, ffee = fee ,
            fstatus = status , fcreatetime =  createtime ,ffinishtime = finishtime)
        self._sqlengine().insert([record])

    @ERROR_CATCH_RAISE
    def updateUserPassword(self,userEmailCrc = None,userNewPassword = None, userNewPasswordCrc = None):
        table = PCE_ACCOUNTS
        qrs = {}
        qrs["fuseremail_crc"] = userEmailCrc
        updateItem = {}
        updateItem["fpassword_crc"] = userNewPasswordCrc
        updateItem["fpassword"] = userNewPassword
        self._sqlengine().update(table, qrs, **updateItem)


    @ERROR_CATCH_RAISE
    def queryFundsByEmailCrc(self,amount,userEmailCrc = None):
        table = PCE_USER_FUNDS
        qrs = {}
        qrs['fuseremail_crc'] = userEmailCrc
        _, result = self._sqlengine().query(table, **qrs)
        return result

    @ERROR_CATCH_RAISE
    def UploadGameInfo(self,gamename = "",gamenamecrc = 0, ishomegust = 0, hometeam = "",hometeamCrc = 0,
            guestteam = "",guestteamCrc = 0,starttime = datetime.utcnow()):
        table = PCE_GAME_INFO
        record = table(fgamename = gamename, fgamename_crc = gamenamecrc, fishomeguest = ishomegust,fhometeam = hometeam,
            fhometeam_crc = hometeamCrc, fguestteam = guestteam, fguestteam_crc = guestteamCrc,
            fstarttime = starttime,fcreatetime =  datetime.utcnow() ,ffinishtime =  datetime.utcnow())
        self._sqlengine().insert([record])

    @ERROR_CATCH_RAISE
    def queryGameInformation(self,name="",skip=0,limit=10):
        table = PCE_GAME_INFO
        try:
            session = self._sqlengine().session()
            retList = []
            result = session.query(table).filter_by(fgamename == name).order_by(table.fstarttime.desc())[skip:skip+limit]
            for it in result:
                game = {}
                game["gameName"] = it.fgamename
                game["gameNameCrc"] = it.fgamename_crc
                game["fishomeguest"] = it.fishomeguest
                game["fhometeam"] = it.fhometeam
                game["fguestteam"] = it.fguestteam
                game["fhomescore"] = it.fhomescore
                game["fguestscore"] = it.fguestscore
                game["fstarttime"] = it.fstarttime
                game["fisOver"] = it.fisOver
                game["ffinishtime"] = it.ffinishtime
                retList.append(game)
            return retList
        except Exception as err:
            session.rollback()
            logging.error("queryGameBriefInformation error")
            raise SqlDatabaseError()
        finally:
            session.close()

    @ERROR_CATCH_RAISE
    def saveBetInfo(self,gamename = "",gamenamecrc = 0,hometeam = "",
            hometeamCrc = 0,guestteam = "",guestteamCrc = 0,starttime = datetime.utcnow(),
            useremail = "",useremailCrc = 0,amount = 0,betside =0):
        table = PCE_BET_INFO
        record = table(fgamename = gamename, fgamename_crc = gamenamecrc, fhometeam = hometeam,hometeam_crc=hometeamCrc,
            fguestteam = guestteam,fguestteam_crc = guestteamCrc, fgamestarttime = starttime,
            fuseremail = useremail, fuseremail_crc = useremailCrc, famount = amount ,fprofitlossamount = Decimal(),
            fbetside = betside, fcreatetime =  datetime.utcnow() ,ffinishtime =  datetime.utcnow())
        self._sqlengine().insert([record])

    @ERROR_CATCH_RAISE
    def saveGameResult(self,gamenamecrc = 0,hometeamCrc = 0,guestteamCrc = 0,
            starttime = datetime.utcnow(),homecore = 0,guestscore = 0):
        table = PCE_GAME_INFO
        conds = {}
        conds["fgamename_crc"] = gamenamecrc
        conds["fhometeam_crc"] = hometeamCrc
        conds["fguestteam_crc"] = guestteamCrc
        conds["fstarttime"] = starttime
        updateItem = {}
        updateItem["fhomescore"] = homecore
        updateItem["fguestscore"] = guestscore
        updateItem["fisOver"] = 1
        updateItem["ffinishtime"] = datetime.utcnow()
        self._sqlengine().update(table, qrs, **updateItem)

    @ERROR_CATCH_RAISE
    def getGameDetailAmount(self,gamenamecrc = gnameCrc,hometeamCrc = hteamCrc,
            guestteamCrc = gteamCrc,starttime = gstarttime):
        table = PCE_BET_INFO
        conds = {}
        conds["fgamename_crc"] = gamenamecrc
        conds["fhometeam_crc"] = hometeamCrc
        conds["fguestteam_crc"] = guestteamCrc
        conds["fstarttime"] = starttime
        _, result = self._sqlengine().query(table, **qrs)
        supHomeAmount = Decimal()
        supHomecount = 0
        supGuestAmount = Decimal()
        supGuestcount = 0
        supTieAmount = Decimal()
        supTiecount = 0
        userBetInfo = {}
        for it in  result:
            if it.fbetside == 0:
                supHomeAmount += it.famount
                supHomecount += 1
            elif it.fbetside == 1:
                supGuestAmount += it.famount
                supGuestcount += 1
            else:
                supTieAmount += it.famount
                supTiecount += 1
            useremail = it.fuseremail
            if isinstance(useremail,bytearray):
                useremail = useremail.decode("utf8")
            userBetInfo[useremail] = {"amount":it.famount,"betside":it.fbetside}
        return supHomecount,supGuestcount,supTiecount,supHomeAmount,supGuestAmount,supTieAmount,userBetInfo

    @ERROR_CATCH_RAISE
    def saveBetResult(self,gamenamecrc = 0,hometeamCrc = 0,guestteamCrc = 0,starttime = datetime.utcnow(),
            homecore = 0,guestscore = 0,winside = None, winfee = None):
        table = PCE_BET_INFO
        try:
            session = self._sqlengine().session()
            conds = {}
            conds["fgamename_crc"] = gamenamecrc
            conds["fhometeam_crc"] = hometeamCrc
            conds["fguestteam_crc"] = guestteamCrc
            conds["fstarttime"] = starttime
            updateItem = {}
            updateItem["fhometeam"] = homecore
            updateItem["fgamename"] = guestscore
            updateItem["fisOver"] = 1
            updateItem["ffinishtime"] = datetime.utcnow()
            records = session.query(table).filter_by(**conds).all()
            for record in records:
                setattr(record, key, value) for key, value in updateItem.items()]
                if record.fbetside == winside:
                    record.fbetresult = 1
                    record.fprofitlossamount = winfee
                else:
                    record.fbetresult = 0
            session.commit()
        except Exception as err:
            session.rollback()
            logging.error("saveBetResult error")
            raise SqlDatabaseError()
        finally:
            session.close()

    @ERROR_CATCH_RAISE
    def updateBetFunds(self,userBetInfo,winSide,winFee):
        table = PCE_USER_FUNDS
        try:
            session = self._sqlengine().session()
            result = session.query(table).filter(table.fuseremail.in_(list(userBetInfo.keys()))).all()
            for it in result:
                useremail = it.fuseremail
                betfreeze = it.fuserbetfreeze
                userallfunds = it.fuserallfunds
                if isinstance(useremail,bytearray):
                    useremail = useremail.decode("utf8")
                it.fuserbetfreeze = betfreeze - userBetInfo[useremail]["amount"]
                if userBetInfo[useremail]["betside"] != winSide:
                    it.fuserallfunds = userallfunds - userBetInfo[useremail]["amount"]
                else:
                    it.fuserallfunds = userallfunds + winFee
        except Exception as err:
            session.rollback()
            logging.error("updateBetFunds error")
            raise SqlDatabaseError()
        finally:
            session.close()

    @ERROR_CATCH_RAISE
    def queryBetHistory(self,emailCrc="",skip,=0,limit=10):
        table = PCE_BET_INFO
        try:
            session = self._sqlengine().session()
            retList = []
            result = session.query(table).filter_by(fuseremail_crc == emailCrc).order_by(table.fcreatetime.desc())[skip:skip+limit]
            for it in result:
                game = {}
                game["gameName"] = it.fgamename
                game["ishomeguest"] = it.fishomeguest
                game["hometeam"] = it.fhometeam
                game["guestteam"] = it.fguestteam
                game["homescore"] = it.fhomescore
                game["guestscore"] = it.fguestscore
                game["starttime"] = it.fgamestarttime
                game["amount"] = it.famount
                game["betside"] = it.fbetside
                game["isOver"] = it.fisOver
                game["finishtime"] = it.ffinishtime
                game["fbetresult"] = it.fbetresult
                game["profitlossamount"] = it.fprofitlossamount
                retList.append(game)
            return retList
        except Exception as err:
            session.rollback()
            logging.error("queryGameBriefInformation error")
            raise SqlDatabaseError()
        finally:
            session.close()
