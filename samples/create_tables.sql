-- CREATE TABLE People (
--     pname varchar(30),
--     amount numeric,
--     bday date,
--     email text,
--     phone varchar(20)    
-- );
CREATE TABLE People (
    pname varchar(30),
    amount float,
    bday varchar(10),
    email varchar(40),
    phone varchar(20)    
);
.mode csv
.import csv_test.csv People
.save sql_test.db