create table Book(
bid char(8) Primary Key,
bname varchar(100) NOT NULL, 
author varchar(50), 
price float, 
bstatus int DEFAULT 0, 
borrow_Times int DEFAULT 0, 
reserve_Times int DEFAULT 0
);

create table Reader(
rid char(8) Primary Key, 
rname varchar(20), 
age int, 
address varchar(100)
);

create table Borrow(
book_ID char(8), 
reader_ID char(8), 
borrow_Date date, 
return_Date date,
Constraint PK_Borrow Primary Key(book_ID, reader_ID, borrow_Date),
Constraint FK_Borrow_Book Foreign Key(book_ID) References Book(bid),
Constraint FK_Borrow_reader Foreign Key(reader_ID) References Reader(rid)
);

create table Reserve(
book_ID char(8), 
reader_ID char(8), 
reserve_Date date DEFAULT (curdate()), 
take_Date date,
Constraint PK_Reserve Primary Key(book_ID, reader_ID, reserve_Date),
Constraint CK_Reserve_TakeDate Check(take_Date > reserve_Date)
);