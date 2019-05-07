-- InnoDb:事物和回滚  uff8mb4 支持更多字符集
-- 索引 提高查询速度而不用去便利整个表。有索引文件。insert update也会操作索引文件
-- 唯一索引 索引列不允许重复值 但是允许为空值  主键不能为空值  唯一索引不能作为其他表的外键
-- BINARY binary属性只用于char和varchar值。当为列指定了该属性时，排序的时候将以区分大小写的方式。与之相反，忽略binary属性时，将使用不区分大小写的方式排序
-- CRC 对比字符串字段建立索引 查询效率更高  而且也安全(虽然可能没必要) 所以对于要建索引的字符串字段最好crc一下



-- ----------------------------
-- Table structure for PCE_ACCOUNTS
-- ----------------------------
-- DROP TABLE IF EXISTS `PCE_ACCOUNTS`;
CREATE TABLE IF NOT EXISTS `PCE_ACCOUNTS` (
  `fid` int(11) NOT NULL AUTO_INCREMENT,
  `fuseremail` varchar(50) BINARY NOT NULL COMMENT '用户邮箱',
  `fuseremail_crc` int(11) unsigned NOT NULL COMMENT '用户邮箱 crc32',
  `fpassword` varchar(50) NOT NULL COMMENT '用户密码',
  `fpassword_crc` int(11) unsigned NOT NULL COMMENT '用户密码 crc32',
  `faddress` varchar(128) BINARY NOT NULL COMMENT '用户地址',
  `faddress_crc` int(11) unsigned NOT NULL COMMENT '用户地址 crc32',
  `fprivatekey` varchar(128) NOT NULL COMMENT '地址私钥',
  `fcreatetime` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `PCE_ACCOUNTS` ADD INDEX INDEX_ACCOUNT_EMAILCRC(fuseremail_crc);
ALTER TABLE `PCE_ACCOUNTS` ADD INDEX INDEX_ACCOUNT_ADDRCRC(faddr_crc);
ALTER TABLE `PCE_ACCOUNTS` ADD INDEX INDEX_ACCOUNT_PASSWORDCRC(fpassword_crc);
--  感觉有必要为地址和邮箱搞成唯一索引

-- ----------------------------
-- Table structure for PCE_USER_FUNDS
-- ----------------------------
-- DROP TABLE IF EXISTS `PCE_USER_FUNDS`;
CREATE TABLE IF NOT EXISTS `PCE_USER_FUNDS` (
  `fid` int(11) NOT NULL AUTO_INCREMENT,
  `fuseremail` varchar(50) BINARY NOT NULL COMMENT '用户邮箱',
  `fuseremail_crc` int(11) unsigned NOT NULL COMMENT '用户邮箱 crc32',
  `faddress` varchar(128) BINARY NOT NULL COMMENT '用户地址',
  `faddress_crc` int(11) unsigned NOT NULL COMMENT '用户地址 crc32',
  `fuserallfunds` decimal(38,8) NOT NULL COMMENT '用户资产',
  `fuserwithdrawfreeze` decimal(38,8) NOT NULL COMMENT '提币冻结',
  `fuserbetfreeze` decimal(38,8) NOT NULL COMMENT '下注冻结',
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `PCE_USER_FUNDS` ADD INDEX INDEX_FUNDS_ADDRCRC(faddr_crc);
ALTER TABLE `PCE_USER_FUNDS` ADD INDEX INDEX_FUNDS_EMAIL(fuseremail);
ALTER TABLE `PCE_USER_FUNDS` ADD INDEX INDEX_FUNDS_EMAILCRC(fuseremail_crc);
-- 用户邮箱是唯一索引


-- ----------------------------
-- Table structure for PCE_BOOS_INFO
-- ----------------------------
-- DROP TABLE IF EXISTS `PCE_BOOS_INFO`;
CREATE TABLE IF NOT EXISTS `PCE_BOOS_INFO` (
  `fid` int(11) NOT NULL AUTO_INCREMENT,
  `ftype` tinyint(4) NOT NULL COMMENT '钱包地址类型,0提币地址暂时也是归集地址,1盈利地址',
  `fvalid` tinyint(4) DEFAULT 1 COMMENT '是否有效 1有效 0 无效',
  `faddress` varchar(128) BINARY NOT NULL COMMENT '地址',
  `faddress_crc` int(11) unsigned NOT NULL COMMENT '地址 crc32',
  `fprivatekey` varchar(128) NOT NULL COMMENT '地址私钥',
  `fcreatetime` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `PCE_BOOS_INFO` ADD INDEX INDEX_BOOS_ADDRCRC(faddr_crc);


-- ----------------------------
-- Table structure for PCE_WITHDRAW
-- ----------------------------
-- DROP TABLE IF EXISTS `PCE_WITHDRAW`;
CREATE TABLE IF NOT EXISTS `PCE_WITHDRAW` (
  `fid` bigint(11) NOT NULL,
  `fheight` bigint(11) NOT NULL COMMENT '区块高度',
  `ftxid` varchar(128) BINARY NOT NULL COMMENT '交易id',
  `ftxid_crc` int(11) unsigned DEFAULT 0 COMMENT '交易id crc32',
  `ffromaddr` varchar(128) BINARY NOT NULL COMMENT '提币地址',
  `ffromaddr_crc` int(11) unsigned DEFAULT 0 COMMENT '提币地址crc32',
  `ftoaddr` varchar(128) BINARY NOT NULL COMMENT '目的地址',
  `ftoaddr_crc` int(11) unsigned DEFAULT 0 COMMENT '目的地址crc32',
  `fvalue` decimal(38,18) NOT NULL COMMENT '提币金额',
  `ffee` decimal(38,18) NOT NULL COMMENT '提币交易费用',
  `fstatus` tinyint(4) NOT NULL COMMENT '是否上链（0否,1是)',
  `fcreatetime` datetime NOT NULL COMMENT '创建时间',
  `ffinishtime` datetime NOT NULL COMMENT '完成时间',
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `PCE_WITHDRAW` ADD INDEX INDEX_WITHDRAW_HEIGHT(fheight);
ALTER TABLE `PCE_WITHDRAW` ADD INDEX INDEX_WITHDRAW_TXID(ftxid_crc);
ALTER TABLE `PCE_WITHDRAW` ADD INDEX INDEX_WITHDRAW_FROM(ffromaddr_crc);
ALTER TABLE `PCE_WITHDRAW` ADD INDEX INDEX_WITHDRAW_TO(ftoaddr_crc);

-- ----------------------------
-- Table structure for PCE_DEPOSIT
-- ----------------------------
-- DROP TABLE IF EXISTS `PCE_DEPOSIT`;
CREATE TABLE IF NOT EXISTS `PCE_DEPOSIT` (
  `fid` bigint(11) NOT NULL,
  `fheight` bigint(11) NOT NULL COMMENT '区块高度',
  `ftxid` varchar(128) BINARY NOT NULL COMMENT '交易id',
  `ftxid_crc` int(11) unsigned DEFAULT 0 COMMENT '交易id crc32',
  `ffromaddr` varchar(128) BINARY NOT NULL COMMENT '充币来源地址',
  `ftoaddr` varchar(128) BINARY NOT NULL COMMENT '充币地址',
  `ftoaddr_crc` int(11) unsigned DEFAULT 0 COMMENT '充币地址crc32',
  `fvalue` decimal(38,18) NOT NULL COMMENT '充币金额',
  `ffee` decimal(38,18) NOT NULL COMMENT '充币费用',
  `fstatus` tinyint(4) NOT NULL COMMENT '是否达到确认数（0否,1是)',
  `fcreatetime` datetime NOT NULL COMMENT '创建时间',
  `ffinishtime` datetime NOT NULL COMMENT '完成时间',
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `PCE_DEPOSIT` ADD INDEX INDEX_DEPOSIT_HEIGHT(fheight);
ALTER TABLE `PCE_DEPOSIT` ADD INDEX INDEX_DEPOSIT_TXID(ftxid_crc);
ALTER TABLE `PCE_DEPOSIT` ADD INDEX INDEX_DEPOSIT_TO(ftoaddr_crc);


-- ----------------------------
-- Table structure for PCE_GAME_INFO
-- ----------------------------
-- DROP TABLE IF EXISTS `PCE_GAME_INFO`;
CREATE TABLE IF NOT EXISTS `PCE_GAME_INFO` (
  `fid` bigint(11) NOT NULL,
  `fgamename` varchar(128) BINARY NOT NULL COMMENT '赛事名',
  `fgamename_crc` int(11) unsigned DEFAULT 0 COMMENT '赛事名 crc32',
  `fishomeguest` tinyint(4) NOT NULL COMMENT '是否是主客场比赛（0否,1是)',
  `fhometeam` varchar(128) BINARY NOT NULL COMMENT '主队名 如果不是主客场比赛那么就是队名大的队伍',
  `fhometeam_crc` int(11) unsigned DEFAULT 0 COMMENT '赛事名 crc32',
  `fguestteam` varchar(128) BINARY NOT NULL COMMENT '客队名',
  `fguestteam_crc` int(11) unsigned DEFAULT 0 COMMENT '赛事名 crc32',
  `fhomescore` int(11) unsigned DEFAULT 0 COMMENT '主队得分',
  `fguestscore` int(11) unsigned DEFAULT 0 COMMENT '客队得分',
  `fstarttime` datetime NOT NULL COMMENT '比赛开始时间',
  `fisOver` tinyint(4) NOT NULL DEFAULT 0 COMMENT '是否已经开奖（0否,1是)',
  `ffinishtime` datetime NOT NULL COMMENT '开奖时间',
  `fcreatetime` datetime NOT NULL COMMENT '创建比赛信息时间',
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `PCE_GAME_INFO` ADD INDEX INDEX_GAMEINFO_NAME(fgamename_crc);
ALTER TABLE `PCE_GAME_INFO` ADD INDEX INDEX_GAMEINFO_HOME(fhometeam_crc);
ALTER TABLE `PCE_GAME_INFO` ADD INDEX INDEX_GAMEINFO_GUEST(fguestteam_crc);
ALTER TABLE `PCE_GAME_INFO` ADD INDEX INDEX_GAMEINFO_TIME(fstarttime);

-- ----------------------------
-- Table structure for PCE_BET_INFO
-- ----------------------------
-- DROP TABLE IF EXISTS `PCE_BET_INFO`;
CREATE TABLE IF NOT EXISTS `PCE_BET_INFO` (
  `fid` bigint(11) NOT NULL,
  `fgamename` varchar(128) BINARY NOT NULL COMMENT '赛事名',
  `fgamename_crc` int(11) unsigned DEFAULT 0 COMMENT '赛事名 crc32',
  `fishomeguest` tinyint(4) NOT NULL COMMENT '是否是主客场比赛（0否,1是)',
  `fhometeam` varchar(128) BINARY NOT NULL COMMENT '主队名 如果不是主客场比赛那么就是队名大的队伍',
  `fhometeam_crc` int(11) unsigned DEFAULT 0 COMMENT '赛事名 crc32',
  `fguestteam` varchar(128) BINARY NOT NULL COMMENT '客队名',
  `fguestteam_crc` int(11) unsigned DEFAULT 0 COMMENT '赛事名 crc32',
  `fhomescore` int(11) unsigned DEFAULT 0 COMMENT '主队得分',
  `fguestscore` int(11) unsigned DEFAULT 0 COMMENT '客队得分',
  `fgamestarttime` datetime NOT NULL COMMENT '比赛开始时间',
  `fuseremail` varchar(50) BINARY NOT NULL COMMENT '用户邮箱',
  `fuseremail_crc` int(11) unsigned NOT NULL COMMENT '用户邮箱 crc32',
  `fcreatetime` datetime NOT NULL COMMENT '下注时间',
  `famount` decimal(38,18) NOT NULL COMMENT '下注金额',
  `fbetside` tinyint(4) NOT NULL DEFAULT 0 COMMENT '下注信息（0A胜,1B胜,2平)',
  `fbetresult` tinyint(4) NOT NULL DEFAULT 2 COMMENT '输赢（0输,1赢,2待开奖)',
  `fprofitlossamount` decimal(38,18) NOT NULL COMMENT '盈亏金额 取决于fbetresult 0待开奖 ',
  `fisOver` tinyint(4) NOT NULL DEFAULT 0 COMMENT '是否已经开奖（0否,1是)',
  `ffinishtime` datetime NOT NULL COMMENT '开奖时间',
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `PCE_BET_INFO` ADD INDEX INDEX_BET_NAME(fgamename_crc);
ALTER TABLE `PCE_BET_INFO` ADD INDEX INDEX_STARTTIME_NAME(fgamestarttime);
ALTER TABLE `PCE_BET_INFO` ADD INDEX INDEX_HOME_NAME(fhometeam_crc);
ALTER TABLE `PCE_BET_INFO` ADD INDEX INDEX_GUEST_NAME(fguestteam_crc);
ALTER TABLE `PCE_BET_INFO` ADD INDEX INDEX_EMAIL_NAME(fuseremail_crc);
