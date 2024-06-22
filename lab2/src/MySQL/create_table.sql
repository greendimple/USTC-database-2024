
use library;
drop table if exists Borrow;
drop table if exists Book;
create table Book(
bid char(8) Primary Key,
bname varchar(100) NOT NULL, 
author varchar(50), 
price float, 
bstatus int DEFAULT 1, -- 1可借 0借出
borrow_Times int DEFAULT 0
);

drop table if exists Reader;
create table Reader(
rid varchar(20), 
rpassword varchar(20),
rname varchar(20), 
age int DEFAULT NULL, 
address varchar(100) DEFAULT NULL,
Constraint PK_Reader Primary Key(rid)
);

drop table if exists Manager;
create table Manager(
mid char(20), 
mpassword varchar(20),
mname varchar(20), 
age int, 
address varchar(100),
Constraint PK_Reader Primary Key(mid)
);


create table Borrow( -- 借书信息
book_ID char(8), 
reader_ID char(20), 
borrow_Date date, 
return_Date date DEFAULT NULL,
Constraint PK_Borrow Primary Key(book_ID, reader_ID, borrow_Date),
Constraint FK_Borrow_Book Foreign Key(book_ID) References Book(bid) on delete cascade,
Constraint FK_Borrow_reader Foreign Key(reader_ID) References Reader(rid) on delete cascade
);
