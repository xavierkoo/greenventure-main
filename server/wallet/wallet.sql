/******************************************************************************/
-- walletDB script
/******************************************************************************/

DROP DATABASE IF EXISTS walletDB;
CREATE DATABASE IF NOT EXISTS walletDB;

USE walletDB;

CREATE TABLE IF NOT EXISTS `WALLET`(
    `walletID` INT AUTO_INCREMENT,
    `userID` VARCHAR(50),
    `points_remaining` INT,
    CONSTRAINT wallet_pk PRIMARY KEY (`walletID`)
);

CREATE TABLE IF NOT EXISTS `WALLETVOUCHER`(
    `walletID` INT,
    `voucherID` VARCHAR(20),
    `voucher_code` VARCHAR(20),
    `used` boolean,
    CONSTRAINT walletvoucher_pk PRIMARY KEY (`walletID`, `voucherID`,`voucher_code`),
    CONSTRAINT walletvoucher_fk1 FOREIGN KEY (`walletID`) REFERENCES `WALLET` (`walletID`)
);


-- inserting mock data

INSERT INTO `WALLET` (`userID`,`points_remaining`) VALUES('162804203307686',100);
INSERT INTO `WALLET` (`userID`,`points_remaining`) VALUES('162804203307687',50);
INSERT INTO `WALLET` (`userID`,`points_remaining`) VALUES('162804203307689',300);

INSERT INTO `WALLETVOUCHER` VALUES('00001','00001','2303FAIRPRICE5', false);
INSERT INTO `WALLETVOUCHER` VALUES('00001','00002','2303GONGCHA1', false);
INSERT INTO `WALLETVOUCHER` VALUES('00003','00003','2303LIHO2', false);
