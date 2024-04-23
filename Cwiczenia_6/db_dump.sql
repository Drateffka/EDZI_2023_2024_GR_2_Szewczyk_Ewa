PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE CurrencyInfo(
            currency_code TEXT PRIMARY KEY, 
            currency_name TEXT
            );
INSERT INTO CurrencyInfo VALUES('USD','dolar amerykański');
INSERT INTO CurrencyInfo VALUES('EUR','euro');
INSERT INTO CurrencyInfo VALUES('CHF','frank szwajcarski');
INSERT INTO CurrencyInfo VALUES('GBP','funt szterling');
INSERT INTO CurrencyInfo VALUES('JPY','jen (Japonia)');
CREATE TABLE CurrencyData(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mid REAL,
            source_table TEXT, 
            effective_date TEXT, 
            currency_code TEXT, 
            FOREIGN KEY(currency_code) REFERENCES CurrencyInfo(currency_code)
            );
INSERT INTO CurrencyData VALUES(0,3.9866000000000001435,'056/A/NBP/2024','2024-03-19','USD');
INSERT INTO CurrencyData VALUES(1,3.9894999999999999573,'057/A/NBP/2024','2024-03-20','USD');
INSERT INTO CurrencyData VALUES(2,3.9430999999999997385,'058/A/NBP/2024','2024-03-21','USD');
INSERT INTO CurrencyData VALUES(3,3.9927999999999999047,'059/A/NBP/2024','2024-03-22','USD');
INSERT INTO CurrencyData VALUES(4,3.9832999999999998408,'060/A/NBP/2024','2024-03-25','USD');
INSERT INTO CurrencyData VALUES(5,3.9704000000000000625,'061/A/NBP/2024','2024-03-26','USD');
INSERT INTO CurrencyData VALUES(6,3.9856999999999999317,'062/A/NBP/2024','2024-03-27','USD');
INSERT INTO CurrencyData VALUES(7,4.008099999999999774,'063/A/NBP/2024','2024-03-28','USD');
INSERT INTO CurrencyData VALUES(8,3.9885999999999999232,'064/A/NBP/2024','2024-03-29','USD');
INSERT INTO CurrencyData VALUES(9,4.0008999999999996788,'065/A/NBP/2024','2024-04-02','USD');
INSERT INTO CurrencyData VALUES(10,3.9843000000000001747,'066/A/NBP/2024','2024-04-03','USD');
INSERT INTO CurrencyData VALUES(11,3.9514999999999997015,'067/A/NBP/2024','2024-04-04','USD');
INSERT INTO CurrencyData VALUES(12,3.9571000000000001506,'068/A/NBP/2024','2024-04-05','USD');
INSERT INTO CurrencyData VALUES(13,3.9546000000000001151,'069/A/NBP/2024','2024-04-08','USD');
INSERT INTO CurrencyData VALUES(14,3.9222999999999998976,'070/A/NBP/2024','2024-04-09','USD');
INSERT INTO CurrencyData VALUES(15,3.9264000000000001122,'071/A/NBP/2024','2024-04-10','USD');
INSERT INTO CurrencyData VALUES(16,3.9706999999999998962,'072/A/NBP/2024','2024-04-11','USD');
INSERT INTO CurrencyData VALUES(17,3.998300000000000054,'073/A/NBP/2024','2024-04-12','USD');
INSERT INTO CurrencyData VALUES(18,4.0209000000000001406,'074/A/NBP/2024','2024-04-15','USD');
INSERT INTO CurrencyData VALUES(19,4.0686999999999997612,'075/A/NBP/2024','2024-04-16','USD');
INSERT INTO CurrencyData VALUES(20,4.0740999999999996106,'076/A/NBP/2024','2024-04-17','USD');
INSERT INTO CurrencyData VALUES(21,4.0559000000000002827,'077/A/NBP/2024','2024-04-18','USD');
INSERT INTO CurrencyData VALUES(22,4.0688000000000004163,'078/A/NBP/2024','2024-04-19','USD');
INSERT INTO CurrencyData VALUES(23,4.05400000000000027,'079/A/NBP/2024','2024-04-22','USD');
INSERT INTO CurrencyData VALUES(24,4.0609999999999999431,'080/A/NBP/2024','2024-04-23','USD');
INSERT INTO CurrencyData VALUES(25,4.4885999999999999232,'056/A/NBP/2024','2024-03-19','CHF');
INSERT INTO CurrencyData VALUES(26,4.4771000000000000795,'057/A/NBP/2024','2024-03-20','CHF');
INSERT INTO CurrencyData VALUES(27,4.4069000000000002614,'058/A/NBP/2024','2024-03-21','CHF');
INSERT INTO CurrencyData VALUES(28,4.4336999999999999744,'059/A/NBP/2024','2024-03-22','CHF');
INSERT INTO CurrencyData VALUES(29,4.437100000000000044,'060/A/NBP/2024','2024-03-25','CHF');
INSERT INTO CurrencyData VALUES(30,4.4047000000000000596,'061/A/NBP/2024','2024-03-26','CHF');
INSERT INTO CurrencyData VALUES(31,4.4017999999999997129,'062/A/NBP/2024','2024-03-27','CHF');
INSERT INTO CurrencyData VALUES(32,4.4227999999999996205,'063/A/NBP/2024','2024-03-28','CHF');
INSERT INTO CurrencyData VALUES(33,4.4249999999999998223,'064/A/NBP/2024','2024-03-29','CHF');
INSERT INTO CurrencyData VALUES(34,4.4036999999999997257,'065/A/NBP/2024','2024-04-02','CHF');
INSERT INTO CurrencyData VALUES(35,4.3875000000000001776,'066/A/NBP/2024','2024-04-03','CHF');
INSERT INTO CurrencyData VALUES(36,4.3620999999999998664,'067/A/NBP/2024','2024-04-04','CHF');
INSERT INTO CurrencyData VALUES(37,4.3795999999999999374,'068/A/NBP/2024','2024-04-05','CHF');
INSERT INTO CurrencyData VALUES(38,4.3666999999999998038,'069/A/NBP/2024','2024-04-08','CHF');
INSERT INTO CurrencyData VALUES(39,4.3365999999999997882,'070/A/NBP/2024','2024-04-09','CHF');
INSERT INTO CurrencyData VALUES(40,4.3446999999999995623,'071/A/NBP/2024','2024-04-10','CHF');
INSERT INTO CurrencyData VALUES(41,4.3451000000000004064,'072/A/NBP/2024','2024-04-11','CHF');
INSERT INTO CurrencyData VALUES(42,4.3804999999999996163,'073/A/NBP/2024','2024-04-12','CHF');
INSERT INTO CurrencyData VALUES(43,4.4047000000000000596,'074/A/NBP/2024','2024-04-15','CHF');
INSERT INTO CurrencyData VALUES(44,4.455400000000000027,'075/A/NBP/2024','2024-04-16','CHF');
INSERT INTO CurrencyData VALUES(45,4.4776999999999995694,'076/A/NBP/2024','2024-04-17','CHF');
INSERT INTO CurrencyData VALUES(46,4.4637000000000002231,'077/A/NBP/2024','2024-04-18','CHF');
INSERT INTO CurrencyData VALUES(47,4.4786999999999999033,'078/A/NBP/2024','2024-04-19','CHF');
INSERT INTO CurrencyData VALUES(48,4.4504999999999999005,'079/A/NBP/2024','2024-04-22','CHF');
INSERT INTO CurrencyData VALUES(49,4.4535000000000000142,'080/A/NBP/2024','2024-04-23','CHF');
INSERT INTO CurrencyData VALUES(50,4.3201000000000000511,'056/A/NBP/2024','2024-03-19','EUR');
INSERT INTO CurrencyData VALUES(51,4.3242000000000002657,'057/A/NBP/2024','2024-03-20','EUR');
INSERT INTO CurrencyData VALUES(52,4.3030999999999997029,'058/A/NBP/2024','2024-03-21','EUR');
INSERT INTO CurrencyData VALUES(53,4.3185999999999999943,'059/A/NBP/2024','2024-03-22','EUR');
INSERT INTO CurrencyData VALUES(54,4.3090999999999999303,'060/A/NBP/2024','2024-03-25','EUR');
INSERT INTO CurrencyData VALUES(55,4.3093000000000003524,'061/A/NBP/2024','2024-03-26','EUR');
INSERT INTO CurrencyData VALUES(56,4.3152999999999996916,'062/A/NBP/2024','2024-03-27','EUR');
INSERT INTO CurrencyData VALUES(57,4.3190999999999997172,'063/A/NBP/2024','2024-03-28','EUR');
INSERT INTO CurrencyData VALUES(58,4.3009000000000003893,'064/A/NBP/2024','2024-03-29','EUR');
INSERT INTO CurrencyData VALUES(59,4.2934000000000001051,'065/A/NBP/2024','2024-04-02','EUR');
INSERT INTO CurrencyData VALUES(60,4.2923000000000000042,'066/A/NBP/2024','2024-04-03','EUR');
INSERT INTO CurrencyData VALUES(61,4.2920999999999995822,'067/A/NBP/2024','2024-04-04','EUR');
INSERT INTO CurrencyData VALUES(62,4.2882999999999995566,'068/A/NBP/2024','2024-04-05','EUR');
INSERT INTO CurrencyData VALUES(63,4.2804999999999999715,'069/A/NBP/2024','2024-04-08','EUR');
INSERT INTO CurrencyData VALUES(64,4.2587999999999999189,'070/A/NBP/2024','2024-04-09','EUR');
INSERT INTO CurrencyData VALUES(65,4.2641000000000000014,'071/A/NBP/2024','2024-04-10','EUR');
INSERT INTO CurrencyData VALUES(66,4.2648999999999999133,'072/A/NBP/2024','2024-04-11','EUR');
INSERT INTO CurrencyData VALUES(67,4.2666000000000003922,'073/A/NBP/2024','2024-04-12','EUR');
INSERT INTO CurrencyData VALUES(68,4.285099999999999909,'074/A/NBP/2024','2024-04-15','EUR');
INSERT INTO CurrencyData VALUES(69,4.3197000000000000952,'075/A/NBP/2024','2024-04-16','EUR');
INSERT INTO CurrencyData VALUES(70,4.3353000000000001534,'076/A/NBP/2024','2024-04-17','EUR');
INSERT INTO CurrencyData VALUES(71,4.3308999999999997498,'077/A/NBP/2024','2024-04-18','EUR');
INSERT INTO CurrencyData VALUES(72,4.3315999999999998948,'078/A/NBP/2024','2024-04-19','EUR');
INSERT INTO CurrencyData VALUES(73,4.320299999999999585,'079/A/NBP/2024','2024-04-22','EUR');
INSERT INTO CurrencyData VALUES(74,4.3334999999999999076,'080/A/NBP/2024','2024-04-23','EUR');
INSERT INTO CurrencyData VALUES(75,5.0515999999999996461,'056/A/NBP/2024','2024-03-19','GBP');
INSERT INTO CurrencyData VALUES(76,5.0635000000000003339,'057/A/NBP/2024','2024-03-20','GBP');
INSERT INTO CurrencyData VALUES(77,5.0366999999999997328,'058/A/NBP/2024','2024-03-21','GBP');
INSERT INTO CurrencyData VALUES(78,5.025699999999999612,'059/A/NBP/2024','2024-03-22','GBP');
INSERT INTO CurrencyData VALUES(79,5.0246000000000003993,'060/A/NBP/2024','2024-03-25','GBP');
INSERT INTO CurrencyData VALUES(80,5.0243000000000002103,'061/A/NBP/2024','2024-03-26','GBP');
INSERT INTO CurrencyData VALUES(81,5.0327000000000001733,'062/A/NBP/2024','2024-03-27','GBP');
INSERT INTO CurrencyData VALUES(82,5.0473999999999996646,'063/A/NBP/2024','2024-03-28','GBP');
INSERT INTO CurrencyData VALUES(83,5.0300000000000002486,'064/A/NBP/2024','2024-03-29','GBP');
INSERT INTO CurrencyData VALUES(84,5.0255999999999998451,'065/A/NBP/2024','2024-04-02','GBP');
INSERT INTO CurrencyData VALUES(85,5.0117000000000002657,'066/A/NBP/2024','2024-04-03','GBP');
INSERT INTO CurrencyData VALUES(86,5.0041999999999999815,'067/A/NBP/2024','2024-04-04','GBP');
INSERT INTO CurrencyData VALUES(87,5.000300000000000189,'068/A/NBP/2024','2024-04-05','GBP');
INSERT INTO CurrencyData VALUES(88,4.99150000000000027,'069/A/NBP/2024','2024-04-08','GBP');
INSERT INTO CurrencyData VALUES(89,4.9660000000000001918,'070/A/NBP/2024','2024-04-09','GBP');
INSERT INTO CurrencyData VALUES(90,4.9843000000000001747,'071/A/NBP/2024','2024-04-10','GBP');
INSERT INTO CurrencyData VALUES(91,4.9835000000000002629,'072/A/NBP/2024','2024-04-11','GBP');
INSERT INTO CurrencyData VALUES(92,5.0007000000000001449,'073/A/NBP/2024','2024-04-12','GBP');
INSERT INTO CurrencyData VALUES(93,5.0191999999999996617,'074/A/NBP/2024','2024-04-15','GBP');
INSERT INTO CurrencyData VALUES(94,5.0609000000000001762,'075/A/NBP/2024','2024-04-16','GBP');
INSERT INTO CurrencyData VALUES(95,5.0811999999999999388,'076/A/NBP/2024','2024-04-17','GBP');
INSERT INTO CurrencyData VALUES(96,5.0589000000000003964,'077/A/NBP/2024','2024-04-18','GBP');
INSERT INTO CurrencyData VALUES(97,5.061499999999999666,'078/A/NBP/2024','2024-04-19','GBP');
INSERT INTO CurrencyData VALUES(98,5.0130999999999996674,'079/A/NBP/2024','2024-04-22','GBP');
INSERT INTO CurrencyData VALUES(99,5.0237999999999995992,'080/A/NBP/2024','2024-04-23','GBP');
INSERT INTO CurrencyData VALUES(100,0.026455000000000001847,'056/A/NBP/2024','2024-03-19','JPY');
INSERT INTO CurrencyData VALUES(101,0.026301000000000001044,'057/A/NBP/2024','2024-03-20','JPY');
INSERT INTO CurrencyData VALUES(102,0.026097999999999998976,'058/A/NBP/2024','2024-03-21','JPY');
INSERT INTO CurrencyData VALUES(103,0.02633399999999999963,'059/A/NBP/2024','2024-03-22','JPY');
INSERT INTO CurrencyData VALUES(104,0.026309000000000000163,'060/A/NBP/2024','2024-03-25','JPY');
INSERT INTO CurrencyData VALUES(105,0.026246999999999998109,'061/A/NBP/2024','2024-03-26','JPY');
INSERT INTO CurrencyData VALUES(106,0.026346999999999995978,'062/A/NBP/2024','2024-03-27','JPY');
INSERT INTO CurrencyData VALUES(107,0.026472000000000002195,'063/A/NBP/2024','2024-03-28','JPY');
INSERT INTO CurrencyData VALUES(108,0.026366000000000000547,'064/A/NBP/2024','2024-03-29','JPY');
INSERT INTO CurrencyData VALUES(109,0.026384000000000003005,'065/A/NBP/2024','2024-04-02','JPY');
INSERT INTO CurrencyData VALUES(110,0.026262000000000003119,'066/A/NBP/2024','2024-04-03','JPY');
INSERT INTO CurrencyData VALUES(111,0.026044999999999998152,'067/A/NBP/2024','2024-04-04','JPY');
INSERT INTO CurrencyData VALUES(112,0.026133000000000001783,'068/A/NBP/2024','2024-04-05','JPY');
INSERT INTO CurrencyData VALUES(113,0.026034999999999994813,'069/A/NBP/2024','2024-04-08','JPY');
INSERT INTO CurrencyData VALUES(114,0.025822999999999995957,'070/A/NBP/2024','2024-04-09','JPY');
INSERT INTO CurrencyData VALUES(115,0.025856000000000003424,'071/A/NBP/2024','2024-04-10','JPY');
INSERT INTO CurrencyData VALUES(116,0.025910999999999999587,'072/A/NBP/2024','2024-04-11','JPY');
INSERT INTO CurrencyData VALUES(117,0.026079999999999996518,'073/A/NBP/2024','2024-04-12','JPY');
INSERT INTO CurrencyData VALUES(118,0.026134000000000003893,'074/A/NBP/2024','2024-04-15','JPY');
INSERT INTO CurrencyData VALUES(119,0.02633500000000000174,'075/A/NBP/2024','2024-04-16','JPY');
INSERT INTO CurrencyData VALUES(120,0.026358999999999999097,'076/A/NBP/2024','2024-04-17','JPY');
INSERT INTO CurrencyData VALUES(121,0.026273999999999997356,'077/A/NBP/2024','2024-04-18','JPY');
INSERT INTO CurrencyData VALUES(122,0.026349999999999997868,'078/A/NBP/2024','2024-04-19','JPY');
INSERT INTO CurrencyData VALUES(123,0.026201999999999996404,'079/A/NBP/2024','2024-04-22','JPY');
INSERT INTO CurrencyData VALUES(124,0.026225999999999998202,'080/A/NBP/2024','2024-04-23','JPY');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('CurrencyData',124);
COMMIT;
