DELIMITER //
drop procedure if exists borrowBook;
create procedure borrowBook(this_rid char(8), this_bid char(8), this_borrow_Date date)
BEGIN
declare state int default 0;
declare borrow_num int default 0;
declare is_same_day_borrow int default 0;
declare reserve_count0 int default 0;
declare reserve_count1 int default 0;
declare CONTINUE HANDLER for SQLEXCEPTION set state = 4;

start transaction;
-- (A)一个读者最多只能借阅 3 本图书，意味着如果读者已经借阅了 3 本图书并且未归还则不允许再借书；
select count(*) from Borrow
where reader_ID = this_rid and return_Date IS NULL
into borrow_num;
IF borrow_num > 2 THEN
    set state = 1;
END IF;
-- (B)同一天不允许同一个读者重复借阅同一本读书；
select count(*) from Borrow
where reader_ID = this_rid
and return_Date IS NULL
and borrow_Date = this_borrow_Date
and book_ID = this_bid 
into is_same_day_borrow;
IF is_same_day_borrow > 0 THEN
    set state = 2;
END IF;
-- (C)如果该图书存在预约记录，而当前借阅者没有预约，则不许借阅；
select count(*) from Reserve
where book_ID = this_bid and reader_ID != this_rid
into reserve_count0;
select count(*) from Reserve
where book_ID = this_bid and reader_ID = this_rid
into reserve_count1;

IF reserve_count0 > 0 AND reserve_count1 = 0 THEN
    set state = 3;
END IF;
-- (D)如果借阅者已经预约了该图书，则允许借阅，但要求借阅完成后删除借阅者对该图书的预约记录；
IF reserve_count1 > 0 THEN
    delete from Reserve
    where book_ID = this_bid and reader_ID = this_rid;
END IF;

-- (E)借阅成功后图书表中的 times 加 1，修改 bstatus，并在borrow表中插入相应借阅信息
IF state = 0 THEN
    update Book set borrow_Times = borrow_Times + 1, bstatus = 1 where Book.bid = this_bid;
    insert into Borrow(book_ID, reader_ID, borrow_Date) values(this_bid, this_rid, this_borrow_Date);
    select "借阅成功！";
    COMMIT;
ELSE -- 下面集中处理错误
    CASE state -- 显示字符串error在结果中
        WHEN 1 THEN select "error: 一个读者最多只能借阅 3 本图书"; ROLLBACK;
        WHEN 2 THEN select "error: 同一天不允许同一个读者重复借阅同一本读书"; ROLLBACK;
        WHEN 3 THEN select "error: 该图书存在预约记录，而当前借阅者没有预约"; ROLLBACK;
        WHEN 4 THEN select "error"; ROLLBACK;
        ELSE
            select "借阅成功！";
            COMMIT;
    END CASE;
END IF;

END //
DELIMITER ;


call borrowBook('R001', 'B008', '2024-05-9');

select * from Reserve where reader_ID = 'R001' and book_ID = 'B001';
select borrow_Times, bstatus from Book where bid = 'B001';
call borrowBook('R001', 'B001', '2024-05-9');
select * from Reserve where reader_ID = 'R001' and book_ID = 'B001';
select borrow_Times, bstatus from Book where bid = 'B001';

call borrowBook('R005', 'B008', '2024-05-9');
