-- 3、 设计一个存储过程 updateReaderID,实现对读者表的 ID 的修改
-- （本题要求不得使用外键定义时的 on update cascade 选项,因为该选项不是所有 DBMS 都支持）。
-- 使用该存储过程：将读者ID中‘R006’改为‘R999’。
-- （3-6题中，select对应表展示变化，另外可以select “error”，会显示字符串error在结果中，实现打印错误信息）
DELIMITER //
drop procedure if exists updateReaderID;
create procedure updateReaderID(reader_ID_from char(8), reader_ID_to char(8))
BEGIN
declare state int default 0;
declare CONTINUE HANDLER for SQLEXCEPTION set state = 1;

start transaction;
alter table Borrow
    drop Constraint FK_Borrow_reader;

update Borrow 
set reader_ID = reader_ID_to
where reader_ID = reader_ID_from;

update Reader 
set rid = reader_ID_to
where rid = reader_ID_from;

IF state = 1 THEN
    select "error"; -- 显示字符串error在结果中
    ROLLBACK;
ELSE
    select "修改成功！";
    COMMIT;
END IF;

END //
DELIMITER ;

-- select * from Reader where rid = 'R006'; -- 展示变化
-- select * from Borrow where reader_ID = 'R006'; -- 展示变化
-- call updateReaderID('R006', 'R999');
-- select * from Reader where rid = 'R999'; -- 展示变化
-- select * from Borrow where reader_ID = 'R999'; -- 展示变化
