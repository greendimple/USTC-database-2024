DELIMITER //
drop function if exists getBorrowTimes;
create function getBorrowTimes(rid varchar(20))
returns int
reads sql data
BEGIN
    DECLARE BorrowTimes INT; -- 声明变量
    SELECT count(*) INTO BorrowTimes FROM Borrow WHERE Borrow.reader_ID = rid;
    RETURN BorrowTimes;
END //
DELIMITER ;