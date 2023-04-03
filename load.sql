DROP DATABASE IF EXISTS accountDB;

CREATE DATABASE IF NOT EXISTS accountDB;

use accountDB;

CREATE TABLE IF NOT EXISTS `ACCOUNT` (
    `userID` VARCHAR(50) NOT NULL,
    `name` VARCHAR(20),
    `email` VARCHAR(50),
    CONSTRAINT account_pk PRIMARY KEY (`userID`)
);

INSERT INTO
    `ACCOUNT`
VALUES
    (
        '123456789',
        'Poster',
        'aaronkwah@gmail.com'
    );

INSERT INTO
    `ACCOUNT`
VALUES
    (
        '9876543321',
        'Tom',
        'ray.quek@gmail.com'
    );

DROP DATABASE IF EXISTS communityDB;

CREATE DATABASE IF NOT EXISTS communityDB;

USE communityDB;

CREATE TABLE IF NOT EXISTS `USERPOST`(
    `postID` INT AUTO_INCREMENT,
    `userID` varchar(50),
    `username` varchar(50),
    `post_datetime` DATETIME,
    `post` VARCHAR(200),
    CONSTRAINT userpost_pk PRIMARY KEY (`postID`)
);

CREATE TABLE IF NOT EXISTS `POSTACTIVITY`(
    `postID` INT,
    `activity_datetime` DATETIME,
    `action_user` varchar(50),
    `action_username` varchar(50),
    `activity` VARCHAR(20),
    `comment` VARCHAR(50),
    CONSTRAINT postactivity_pk PRIMARY KEY (`postID`, `activity_datetime`, `action_user`),
    CONSTRAINT postactivity_fk1 FOREIGN KEY (`postID`) REFERENCES `USERPOST` (`postID`)
);

DROP DATABASE IF EXISTS voucherDB;

CREATE DATABASE IF NOT EXISTS voucherDB;

USE voucherDB;

CREATE TABLE IF NOT EXISTS `VOUCHER`(
    `voucherID` INT(5) AUTO_INCREMENT,
    `value` INT,
    `merchant_name` VARCHAR(50),
    `voucher_name` VARCHAR(50),
    `voucher_code` VARCHAR(50),
    `description` VARCHAR(100),
    `pointsRequired` INT,
    `quantity` INT,
    CONSTRAINT voucher_pk PRIMARY KEY (`voucherID`)
);

INSERT INTO
    `VOUCHER` (
        `value`,
        `merchant_name`,
        `voucher_name`,
        `voucher_code`,
        `description`,
        `pointsRequired`,
        `quantity`
    )
VALUES
    (
        5,
        'Fairprice',
        'Fairprice $5 Voucher',
        '2303FAIRPRICE5',
        '$5 OFF total spending, minimum spending of $30 is required',
        2000,
        5000
    );

INSERT INTO
    `VOUCHER` (
        `value`,
        `merchant_name`,
        `voucher_name`,
        `voucher_code`,
        `description`,
        `pointsRequired`,
        `quantity`
    )
VALUES
    (
        1,
        'GongCha',
        'GongCha $1 Voucher',
        '2303GONGCHA1',
        '$1 OFF total spending, minimum spending of $10 is required',
        1000,
        6700
    );

INSERT INTO
    `VOUCHER` (
        `value`,
        `merchant_name`,
        `voucher_name`,
        `voucher_code`,
        `description`,
        `pointsRequired`,
        `quantity`
    )
VALUES
    (
        2,
        'Liho',
        'Liho $2 Voucher',
        '2303LIHO2',
        '$2 OFF total spending, minimum spending of $10 is required',
        1500,
        10000
    );

INSERT INTO
    `VOUCHER` (
        `value`,
        `merchant_name`,
        `voucher_name`,
        `voucher_code`,
        `description`,
        `pointsRequired`,
        `quantity`
    )
VALUES
    (
        5,
        'Redmart',
        'Redmart $5 Voucher',
        '2303REDMART5',
        '$5 OFF total spending, minimum spending of $30 is required',
        1500,
        10000
    );

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
    CONSTRAINT walletvoucher_pk PRIMARY KEY (`walletID`, `voucherID`, `voucher_code`),
    CONSTRAINT walletvoucher_fk1 FOREIGN KEY (`walletID`) REFERENCES `WALLET` (`walletID`)
);

-- inserting mock data
INSERT INTO
    `WALLET` (`userID`, `points_remaining`)
VALUES
    ('162804203307685', 1000);

INSERT INTO
    `WALLET` (`userID`, `points_remaining`)
VALUES
    ('162804203307687', 2000);

INSERT INTO
    `WALLET` (`userID`, `points_remaining`)
VALUES
    ('162804203307689', 2040);

INSERT INTO
    `WALLETVOUCHER`
VALUES
    ('00001', '00001', '2303FAIRPRICE5', false);

INSERT INTO
    `WALLETVOUCHER`
VALUES
    ('00001', '00002', '2303GONGCHA1', false);

INSERT INTO
    `WALLETVOUCHER`
VALUES
    ('00003', '00003', '2303LIHO2', false);

/******************************************************************************/
-- missionDB script
/******************************************************************************/
DROP DATABASE IF EXISTS missionDB;

CREATE DATABASE IF NOT EXISTS missionDB;

USE missionDB;

CREATE TABLE IF NOT EXISTS `MISSION`(
    `missionID` INT(5) NOT NULL AUTO_INCREMENT,
    `reward` INT(5),
    `required_count` INT(3),
    `mission_category` VARCHAR(20),
    `description` VARCHAR(100),
    CONSTRAINT mission_pk PRIMARY KEY (`missionID`)
);

CREATE TABLE IF NOT EXISTS `USERMISSION`(
    `missionID` INT(5),
    `userID` VARCHAR(50),
    `completed_count` INT(3),
    `status` VARCHAR(20),
    CONSTRAINT usermission_pk PRIMARY KEY (`missionID`, `userID`),
    CONSTRAINT usermission_fk1 FOREIGN KEY (`missionID`) REFERENCES `MISSION` (`missionID`)
);

-- inserting mock data
INSERT INTO
    `MISSION` (
        `reward`,
        `mission_category`,
        `required_count`,
        `description`
    )
VALUES
    (
        60,
        'Plastic',
        3,
        'Earn 60 points when you recycle 3 plastic items at our recycling bin!'
    );

INSERT INTO
    `MISSION` (
        `reward`,
        `mission_category`,
        `required_count`,
        `description`
    )
VALUES
    (
        100,
        'Paper',
        5,
        'Earn 100 points when you recycle 5 paper items at our recycling bin!'
    );

INSERT INTO
    `MISSION` (
        `reward`,
        `mission_category`,
        `required_count`,
        `description`
    )
VALUES
    (
        20,
        'Plastic',
        1,
        'Earn 20 points when you recycle 1 plastic item at our recycling bin!'
    );

INSERT INTO
    `MISSION` (
        `reward`,
        `mission_category`,
        `required_count`,
        `description`
    )
VALUES
    (
        200,
        'Electronics',
        2,
        'Earn 200 points when you recycle 2 electronic waste at our recycling bin!'
    );

/******************************************************************************/
-- recyclingbinDB script
/******************************************************************************/
DROP DATABASE IF EXISTS recyclingbinDB;

CREATE DATABASE IF NOT EXISTS recyclingbinDB;

USE recyclingbinDB;

CREATE TABLE IF NOT EXISTS `MISSIONCODE`(
    `mission_category` VARCHAR(20),
    `verification_code` VARCHAR(6),
    `datetime_expire` DATETIME,
    `redeemed` BOOLEAN,
    CONSTRAINT missioncode_pk PRIMARY KEY (
        `mission_category`,
        `verification_code`,
        `datetime_expire`
    )
);

INSERT INTO
    `MISSIONCODE`
VALUES
    ('Plastic', '112492', '2023-02-02 13:23:24', 1);

INSERT INTO
    `MISSIONCODE`
VALUES
    ('Plastic', '639152', '2023-02-03 22:23:24', 1);

INSERT INTO
    `MISSIONCODE`
VALUES
    ('Paper', '679251', '2023-02-03 19:58:12', 0);

INSERT INTO
    `MISSIONCODE`
VALUES
    ('Paper', '242267', '2023-03-03 10:02:54', 0);

CREATE EVENT delete_old_verification_code ON SCHEDULE EVERY 1 DAY DO
DELETE FROM
    MISSIONCODE
WHERE
    datetime_expire < DATE_SUB(NOW(), INTERVAL 1 DAY);