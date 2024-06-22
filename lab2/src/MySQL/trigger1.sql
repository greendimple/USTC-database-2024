DELIMITER //
drop trigger if exists borrowBook1;
create trigger borrowBook1 after INSERT on Borrow for each row
BEGIN
    -- 更改Book表中的bstatus
    update Book set bstatus = 0 where bid = new.book_ID;
END //
DELIMITER ;


DELIMITER //
drop trigger if exists borrowBook2;
create trigger borrowBook2 after INSERT on Borrow for each row
BEGIN
   -- 更改Book表中的borrow_Times
    update Book set borrow_Times=borrow_Times+1 where bid = new.book_ID;
END //
DELIMITER ;
