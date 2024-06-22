DELIMITER //
drop procedure if exists returnBook;
create procedure returnBook(this_rid char(8), this_bid char(8), this_return_Date date)
BEGIN
declare state int default 0;
declare reserve_count int default 0;
declare borrow_count int default 0;
declare CONTINUE HANDLER for SQLEXCEPTION set state = 2;

start transaction;
select count(*) from Reserve
where book_ID = this_bid and reader_ID != this_rid
into reserve_count;

select count(*) from Borrow
where book_ID = this_bid and reader_ID = this_rid and return_Date IS NULL
into borrow_count;

IF borrow_count = 0 THEN
    set state = 1;
END IF;

IF state = 0 THEN
    -- 还书后补上借阅表 borrow 中对应记录的 return_date;
    update Borrow set return_Date = this_return_Date 
    where book_ID = this_bid and reader_ID = this_rid and return_Date IS NULL;
    -- 还书后将图书表 book 中对应记录的 bstatus 修改为 0（没有其他预约）或 2（有其他预约）
    IF reserve_count = 0 THEN
        update Book set bstatus = 0 where bid = this_bid;
    ELSE
        update Book set bstatus = 2 where bid = this_bid;
    END IF;
    select "还书成功！";
    COMMIT;
ELSEIF state = 1 THEN-- 下面集中处理错误
    select "error: 未借阅，还书失败";
    ROLLBACK;
ELSE
    select "error";
    ROLLBACK;
END IF;

END //
DELIMITER ;


call returnBook('R001', 'B008', '2024-05-10');

select * from Book where bid = 'B001';
select * from Borrow where book_ID = 'B001' and reader_ID = 'R001';
call returnBook('R001', 'B001', '2024-05-10');
select * from Book where bid = 'B001';
select * from Borrow where book_ID = 'B001' and reader_ID = 'R001';
