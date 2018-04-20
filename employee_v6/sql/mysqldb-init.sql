# Initialize a mysql db with a 'test' db and be able test productpage with it.
# mysql -h 127.0.0.1 -ppassword < mysqldb-init.sql

CREATE DATABASE test;
USE test;

CREATE TABLE `ratings` (
  `ReviewID` INT NOT NULL,
  `Rating` INT,
  PRIMARY KEY (`ReviewID`)
);
INSERT INTO ratings (ReviewID, Rating) VALUES (1, 5);
INSERT INTO ratings (ReviewID, Rating) VALUES (2, 4);

CREATE TABLE `payroll` (
  `ID` INT NOT NULL,
  `EmpID` INT,
  `Salary` INT,
  `Month` INT,
  PRIMARY KEY (`ID`)
);
INSERT INTO payroll (ID, EmpID, Salary, Month) VALUES (1, 1, 12444, 122017);
INSERT INTO payroll (ID, EmpID, Salary, Month) VALUES (2, 1, 12555, 052018);
