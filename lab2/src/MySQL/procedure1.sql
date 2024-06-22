-- 设计一个存储过程 updateReaderID,实现对读者表的 ID 的修改
DELIMITER //
drop procedure if exists updateReaderID;
create procedure updateReaderID(reader_ID_from varchar(20), reader_ID_to varchar(20))
BEGIN
declare state int default 0;
declare CONTINUE HANDLER for SQLEXCEPTION set state = 1;

-- start transaction;
alter table Borrow
    drop Constraint FK_Borrow_reader;

update Borrow 
set reader_ID = reader_ID_to
where reader_ID = reader_ID_from;

update Reader 
set rid = reader_ID_to
where rid = reader_ID_from;

END //
DELIMITER ;

