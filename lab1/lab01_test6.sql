-- A 当一本书被预约时, 自动将图书表 book 中相应图书的bstatus修改为 2，并增加 reserve_Times；
DELIMITER //
drop trigger if exists reserveBook1;
create trigger reserveBook1 after insert on Reserve for each row
BEGIN
    update Book set bstatus = 2 where bid = new.book_ID;
END //
DELIMITER ;

DELIMITER //
drop trigger if exists reserveBook2;
create trigger reserveBook2 after insert on Reserve for each row
BEGIN
    update Book set reserve_Times = reserve_Times + 1 where bid = new.book_ID;
END //
DELIMITER ;

-- B 当某本预约的书被借出时或者读者取消预约时, 自动减少reserve_Times；
DELIMITER //
drop trigger if exists reserveBook3;
create trigger reserveBook3 after delete on Reserve for each row
BEGIN
    update Book set reserve_Times = reserve_Times - 1 where bid = old.book_ID;
END //
DELIMITER ;

-- C 当某本书的最后一位预约者取消预约且该书未被借出（修改前 bstatus 为 2）时，将 bstatus 改为 0。
DELIMITER //
drop trigger if exists reserveBook4;
create trigger reserveBook4 after delete on Reserve for each row
BEGIN
    declare reserve_count int default 0;
    declare this_bstatus int default 0;

    select count(*) from Reserve
    where book_ID = old.book_ID
    into reserve_count;

    select bstatus from Book
    where bid = old.book_ID 
    into this_bstatus;

    IF reserve_count = 0 and this_bstatus = 2 THEN
        update Book set bstatus = 0 where bid = old.book_ID;
    END IF;

END //
DELIMITER ;


select reserve_Times, bstatus from Book where bid = 'B012';
insert into Reserve(reader_ID, book_ID, reserve_Date)
values('R001', 'B012', '2024-05-9');
select reserve_Times, bstatus from Book where bid = 'B012';

delete from Reserve
where reader_ID = 'R001' and book_ID = 'B012' and reserve_Date = '2024-05-9';
select reserve_Times, bstatus from Book where bid = 'B012';
