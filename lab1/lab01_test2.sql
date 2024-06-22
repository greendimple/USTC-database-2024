-- (1)查询读者 Rose 借过的书（包括已还和未还）的图书号、书名和借期；
Select book_ID, bname, borrow_Date 
from Book, Borrow
where Book.bid = Borrow.book_ID and reader_ID = 'R002';

-- (2)查询从没有借过图书也从没有预约过图书的读者号和读者姓名
Select rid, rname
from Reader
where rid not in (select distinct reader_ID from Borrow) and rid not in (select distinct reader_ID from Reserve);

-- (3)查询被借阅次数最多的作者（注意一个作者可能写了多本书）；
-- （使用两种方法： A.使用借阅表 borrow 中的借书记录；B.使用图书表 book 中的 borrow_times）
-- （思考：哪种方法更好？）
-- A
select t.author from(
select author, count(*) as borrow_count
from Book, Borrow
where Book.bid = Borrow.book_ID
group by author
order by borrow_count desc
limit 1
)t;

-- B
select t.author from(
select author, sum(borrow_Times) as borrow_count
from Book
group by author
order by borrow_count desc
limit 1
)t;  -- B更好，省略了连接查询，效率更高。

-- （4）查询目前借阅未还的书名中包含“MySQL”的图书号和书名；
select bid, bname
from Book, Borrow
where Book.bid = Borrow.book_ID
and return_Date IS NULL
and bname LIKE '%MySQL%';

-- （5）查询借阅图书数目（多次借同一本书需重复计入）超过 3 本的读者姓名；
select t.rname from(
select rname, count(*) as borrow_num
from Reader, Borrow
where rid = reader_ID
group by reader_ID
having borrow_num > 3
)t;

-- （6）查询没有借阅过任何一本 J.K. Rowling 所著的图书的读者号和姓名；
select rid, rname
from Reader
where rid not in(
select distinct reader_ID from Borrow, Book 
where book_ID = bid
and author = 'J.K. Rowling'
);

-- （7）查询 2024 年借阅图书数目排名前 3 名的读者号、姓名以及借阅图书数；
select rid, rname, count(*) as borrow_num
from Reader, Borrow
where rid = reader_ID
group by reader_ID
order by borrow_num desc
limit 3;

-- （8）创建一个读者借书信息的视图，该视图包含读者号、姓名、所借图书号、图书名和借期
-- （对于没有借过图书的读者，是否包含在该视图中均可）；
-- 并使用该视图查询2024年所有读者的读者号以及所借阅的不同图书数；
DROP VIEW IF EXISTS reader_borrow_view;
create view reader_borrow_view
as select rid, rname, book_ID, bname, borrow_Date
from Reader, Book, Borrow
where rid = reader_ID
and bid = book_ID;

select rid, count(*) as borrow_num_diff
from (select distinct book_ID, rid, year(borrow_Date) as borrow_year from reader_borrow_view) as t -- *不同*图书数
where borrow_year = 2024
group by t.rid;


