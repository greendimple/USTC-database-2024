from login_start import Ui_loginWindow
from welcome import Ui_WelcomeWindow
from personal_information import Ui_PersonalnformationWindow
from borrow import Ui_BorrowWindow
from return_book import Ui_ReturnWindow
from manager import Ui_ManagerWindow

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTreeWidgetItem, QLabel, QTableWidgetItem, QPushButton, QFileDialog
from PyQt5.QtCore import QDate, QTime, Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, uic
import sys
import MySQLdb
import os
import shutil
from datetime import datetime

# pyuic5 -o manager.py manager.ui

current_user = ''
today = datetime.today()

class LoginWindow(QMainWindow, Ui_loginWindow):
	def __init__(self):
		super().__init__() #初始化QMainWindows类
		self.welcome_window = None
		self.setupUi(self)
		self.setWindowTitle('图书管理系统-----PB21061224付斯珂')
		self.bind_up()
		
	def bind_up(self):
		self.sign_in_button.clicked.connect(self.sign_in)
		self.sign_up_button.clicked.connect(self.sign_up)
	
	def execute(self, recieve):
		global db
		result = []
		if status == 0:
			cursor = db.cursor()
			try:
				cursor.execute(self.query)
			except:
				self.error_input('SQL执行失败')
				db.rollback()
				return False
			if recieve:  # 有查询结果返回值
				result = cursor.fetchall()
			else: # 无查询结果返回值
				result = cursor.fetchall()
				if(len(result) == 0): 
					result = False
				else: result = True

			db.commit()
			cursor.close()

		self.last = '' #每进行一次操作需要刷新 doubleclicked item时记录的待更改值
		return result
	
	def error_input(self, err_msg):
		QMessageBox.information(self, "错误提示", err_msg, QMessageBox.Yes)

	# 注册
	def sign_up(self):
		if self.lineEdit.text() == '' or self.lineEdit_2.text() == '':
			self.error_input('输入信息不足!')
			return
		self.query = f"select * from reader where rid={self.lineEdit.text()};"
		exist_id = self.execute(False)
		if exist_id: 
			self.error_input('账号已存在!')
			return
		#确认插入reader
		reply = QMessageBox.question(self, '确认', "确定注册?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.No:
			return
		self.query = 'insert into Reader(rid, rpassword) Values(\'{}\', \'{}\');'.format(self.lineEdit.text(), self.lineEdit_2.text())
		self.execute(False)
		global current_user 
		current_user = ((self.lineEdit.text(), None),)
		QMessageBox.information(self, "提示", "注册成功！", QMessageBox.Yes)
		self.welcome_window.pushButton_4.hide()

		self.close()
		self.welcome_window.setWindowTitle("Welcome! ")
		self.welcome_window.show()

	# 登录
	def sign_in(self):
		if self.lineEdit.text() == '' or self.lineEdit_2.text() == '':
			self.error_input('输入信息不足!')
			return
		self.query = 'select rid, rname from Reader where rid=\'{}\' and rpassword=\'{}\';'.format(self.lineEdit.text(), self.lineEdit_2.text())
		global current_user
		current_user = self.execute(True)
		if len(current_user) == 0: 
			self.query = 'select * from Reader where rid=\'{}\';'.format(self.lineEdit.text())
			rid_exist = self.execute(False)
			if rid_exist == False: 
				self.error_input("登录失败！账号不存在")
			else:
				self.error_input("登录失败！密码错误")
		else: 
			# print("登录成功！")
			print(current_user)
			current_user_rname = current_user[0][1]
			
			# 登录成功后检查是否为管理员
			self.check_manager()  # 决定管理员操作button是否显示
			# 关闭登录窗口
			self.close()
			# 根据登录用户名显示导航（欢迎）窗口
			self.welcome_window.setWindowTitle("Welcome! " + str(current_user_rname))
			self.welcome_window.show()
		

	def check_manager(self):
		global current_user
		rid = current_user[0][0]
		self.query = f"select * from Manager where mid='{rid}';"
		is_manager = self.execute(False)
		if is_manager:
			self.welcome_window.pushButton_4.show()
		else:
			self.welcome_window.pushButton_4.hide()


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Window")
        self.label = QLabel("Welcome")
        self.setCentralWidget(self.label)	


class PersonnalInformationWindow(QMainWindow, Ui_PersonalnformationWindow):
	def __init__(self):
		super().__init__()
		self.img_label = QLabel(self)  # 用于显示图片
		self.setupUi(self)
		self.default_img_path = r"D:\codeConfiguration\MySQL\lab2\src\user_pics\default.jpg"
		self.bind_up()

	def bind_up(self):
		# 当输入框中的数据改变，则修改数据库对应条目
		self.lineEdit.textChanged.connect(self.change_age)
		self.lineEdit_2.textChanged.connect(self.change_address)
		self.lineEdit_3.textChanged.connect(self.change_name)
		self.lineEdit_4.textChanged.connect(self.change_rid)
		self.pushButton.clicked.connect(self.change_img)

	def change_rid(self):
		global current_user
		reader_ID_from = current_user[0][0]
		reader_ID_to = self.lineEdit_4.text()
		# 存储过程
		self.query = f"call updateReaderID('{reader_ID_from}', '{reader_ID_to}');"
		self.execute(False)
		# 修改头像文件名
		if(os.path.exists(f"D:/codeConfiguration/MySQL/lab2/src/user_pics/{reader_ID_to}.jpg") and os.path.exists(f"D:/codeConfiguration/MySQL/lab2/src/user_pics/{reader_ID_from}.jpg")):
			os.rename(f"D:/codeConfiguration/MySQL/lab2/src/user_pics/{reader_ID_from}.jpg", f"D:/codeConfiguration/MySQL/lab2/src/user_pics/{reader_ID_to}.jpg")
		# 更新current_user
		current_user = ((reader_ID_to, current_user[0][1]),)
	
	def change_age(self):
		if self.lineEdit.text() == '' or self.lineEdit.text() == 'None': new_age = 'NULL'
		else: new_age = int(self.lineEdit.text())
		self.query = 'update Reader set age={} where rid=\'{}\';'.format(new_age, current_user[0][0])
		self.execute(False)
		
	def change_address(self):
		self.query = 'update Reader set address=\'{}\' where rid=\'{}\';'.format(self.lineEdit_2.text(), current_user[0][0])
		self.execute(False)
	
	def change_name(self):
		global current_user
		self.query = 'update Reader set rname=\'{}\' where rid=\'{}\';'.format(self.lineEdit_3.text(), current_user[0][0])
		self.execute(False)
		current_user = ((current_user[0][0], self.lineEdit_3.text()),)
	
	def error_input(self, err_msg):
		QMessageBox.information(self, "错误提示", err_msg, QMessageBox.Yes)

	def execute(self, recieve):
		global db
		result = []
		if status == 0:
			cursor = db.cursor()
			try:
				cursor.execute(self.query)
			except:
				self.error_input('SQL执行失败')
				db.rollback()
				return False
			if recieve:
				result = cursor.fetchall()
			else:
				result = True
			db.commit()
			cursor.close()

		self.last = '' #每进行一次操作需要刷新 doubleclicked item时记录的待更改值
		return result

	def insert_image(self, image_path):
		if(os.path.exists(image_path)):
			pixmap = QPixmap(image_path)
		else: pixmap = QPixmap(self.default_img_path)  # 加载图片
		pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio)  # 调整图片大小为100x100，同时保持纵横比
		self.img_label.setPixmap(pixmap)  # 设置 QPixmap
		self.img_label.resize(pixmap.width(), pixmap.height())  # 调整 QLabel 的大小以适应图片
		self.img_label.move(25, 120)  # 设置 QLabel 的位置

	def change_img(self):
		image_path_from = QFileDialog.getOpenFileName(self, "选择图片", "C:/", "Image files(*.jpg *.png *.gif *.jpeg *.bmp)")[0]
		if image_path_from:
			self.insert_image(image_path_from)
			# 新图片保存
			rid = current_user[0][0]
			image_path_to = "D:/codeConfiguration/MySQL/lab2/src/user_pics" + "/"+ rid + ".jpg"
			if(os.path.exists(image_path_to)):
				os.remove(image_path_to)
				shutil.copy(image_path_from, image_path_to)
		else: 
			self.insert_image(self.default_img_path)
		
	def show(self):
		global current_user
		current_user_rid = current_user[0][0]
		current_user_rname = current_user[0][1]

		self.query = 'select age from Reader where rid=\'{}\';'.format(current_user_rid)
		current_user_age = self.execute(True)
		current_user_age = current_user_age[0][0]
		self.query = 'select address from Reader where rid=\'{}\';'.format(current_user_rid)
		current_user_address = self.execute(True)
		current_user_address = current_user_address[0][0]

		# 查询数据库中个人信息并显示
		self.lineEdit_4.setText(current_user_rid)
		self.lineEdit_3.setText(str(current_user_rname))
		self.lineEdit.setText(str(current_user_age))
		self.lineEdit_2.setText(str(current_user_address))

		# 头像显示
		img_path = "D:/codeConfiguration/MySQL/lab2/src/user_pics" + "/"+ current_user_rid + ".jpg"
		if(os.path.exists(img_path)):
			self.insert_image(img_path)  # 插入对应用户头像
		else:
			self.insert_image(self.default_img_path)  # 插入默认图片

		super().show()
		

class BorrowWindow(QMainWindow, Ui_BorrowWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.bind_up()
	
	def bind_up(self):
		self.pushButton.clicked.connect(self.search_book)
		self.pushButton_2.clicked.connect(self.lineEdit.clear)
	
	def execute(self, recieve):
		global db
		result = []
		if status == 0:
			cursor = db.cursor()
			try:
				cursor.execute(self.query)
			except:
				self.error_input('SQL执行失败')
				db.rollback()
				return False
			if recieve:
				result = cursor.fetchall()
			else:
				result = True
			db.commit()
			cursor.close()

		self.last = '' #每进行一次操作需要刷新 doubleclicked item时记录的待更改值
		return result
	
	def error_input(self, err_msg):
		QMessageBox.information(self, "错误提示", err_msg, QMessageBox.Yes)
	
	def search_book(self):
		self.query = f"select * from Book where bname LIKE '%{self.lineEdit.text()}%';"
		book_info = self.execute(True)
		if len(book_info) == 0: 
			self.error_input("未找到相关书籍！")
			return
		# self.tableWidget.clear()  # 清空表格上次搜索记录
		self.tableWidget.setRowCount(0)  # 清空表格上次搜索记录
		for row in book_info: 
			i = 0
			bstatus = "可借" if row[4] else "不可借"
			self.tableWidget.insertRow(i)  # 尾部插入一行
			if(row[4] == 0): 
				self.query = f"select borrow_Date from Borrow where book_ID='{row[0]}' and return_Date is NULL;"
				borrow_Date = self.execute(True)
				borrow_Date = borrow_Date[0][0]
				self.tableWidget.setItem(i, 4, QTableWidgetItem(f"{bstatus} 借出日期{str(borrow_Date.year)}-{str(borrow_Date.month)}-{str(borrow_Date.day)}"))
			else: 
				self.tableWidget.setItem(i, 4, QTableWidgetItem(bstatus))
			self.tableWidget.setItem(i, 0, QTableWidgetItem(str(row[0])))  # 设置该行元素
			self.tableWidget.setItem(i, 1, QTableWidgetItem(str(row[1])))
			self.tableWidget.setItem(i, 2, QTableWidgetItem(str(row[2])))
			self.tableWidget.setItem(i, 3, QTableWidgetItem(str(row[3])))
			self.tableWidget.setItem(i, 5, QTableWidgetItem(str(row[5])))
			# 添加借阅按钮
			if(row[4]):
				borrow_buttons = self.__dict__
				borrow_buttons['borrow_button_' + str(i)] = QPushButton('借阅')
				self.tableWidget.setCellWidget(i, 6, borrow_buttons['borrow_button_' + str(i)])  # 假设你想在第8列（索引为7）添加按钮
				borrow_buttons['borrow_button_' + str(i)].clicked.connect(self.borrow_book)
			else :
				self.tableWidget.setItem(i, 6, QTableWidgetItem(''))  # 不可借时不显示按钮
			i += 1

	def borrow_book(self):
		current_row = self.tableWidget.currentRow()
		bid = self.tableWidget.item(current_row, 0).text()
		# # 模拟触发器，以下为借一本书后引发的操作
		# # 1.更改Book表中的bstatus
		# self.query = f"update Book set bstatus=0 where bid ='{bid}';"
		# success = self.execute(False)
		# if success == False:
		# 	self.error_input('借阅失败！')
		# 	return
		# # 2.更改Book表中的borrow_Times
		# self.query = f"update Book set borrow_Times=borrow_Times+1 where bid ='{bid}';"
		# self.execute(False)
		# 3.在Borrow表中插入一条记录
		global current_user
		self.query = f"insert into Borrow(book_ID, reader_ID, borrow_Date) Values('{bid}', '{current_user[0][0]}','{str(today)[:10]}');"
		self.execute(False)
		
		QMessageBox.information(self, "提示", "借阅成功！", QMessageBox.Yes)
		# 更新表格
		self.tableWidget.setItem(current_row, 4, QTableWidgetItem('不可借'))  # 更新状态
		self.tableWidget.setItem(current_row, 7, QTableWidgetItem(''))  # 删除按钮
		# 重新显示搜索结果
		self.search_book()


class ReturnWindow(QMainWindow, Ui_ReturnWindow):
	def __init__(self):
		super().__init__()
		self.search_mode = 0
		self.setupUi(self)
		self.bind_up()
	
	def bind_up(self):
		self.pushButton.clicked.connect(lambda: self.search_book(1))
		self.pushButton_2.clicked.connect(lambda: self.search_book(0))
	
	def execute(self, recieve):
		global db
		result = []
		if status == 0:
			cursor = db.cursor()
			try:
				cursor.execute(self.query)
			except:
				self.error_input('SQL执行失败')
				db.rollback()
				return False
			if recieve:
				result = cursor.fetchall()
			else:
				result = True
			db.commit()
			cursor.close()

		self.last = '' #每进行一次操作需要刷新 doubleclicked item时记录的待更改值
		return result
	
	def error_input(self, err_msg):
		QMessageBox.information(self, "错误提示", err_msg, QMessageBox.Yes)
	
	def search_book(self, mode):
		self.search_mode = mode
		self.tableWidget.setRowCount(0)  # 清空表格上次搜索记录
		if mode == 0:  # 查询所有借阅记录
			self.query = f"select bid, bname, author, price, borrow_Date, return_Date from Borrow, Book where reader_ID='{current_user[0][0]}' and bid=book_id;"
		else:  # 只查询未归还的记录
			self.query = f"select bid, bname, author, price, borrow_Date, return_Date from Borrow, Book where reader_ID='{current_user[0][0]}' and bid=book_id and return_Date is NULL;"
		borrow_info = self.execute(True)
		if len(borrow_info) == 0: 
			if(mode == 0): self.error_input("还没有借过书哦！")
			else: self.error_input("没有未归还的书籍！")
			return
		for row in borrow_info: 
			i = 0
			self.tableWidget.insertRow(i)  # 尾部插入一行
			self.tableWidget.setItem(i, 0, QTableWidgetItem(str(row[0])))  # book_id
			self.tableWidget.setItem(i, 1, QTableWidgetItem(str(row[1])))  # 书名
			self.tableWidget.setItem(i, 2, QTableWidgetItem(str(row[2])))  # 作者
			self.tableWidget.setItem(i, 3, QTableWidgetItem(str(row[3])))  # 价格
			self.tableWidget.setItem(i, 4, QTableWidgetItem(str(row[4])))  # 借入日期
			self.tableWidget.setItem(i, 5, QTableWidgetItem(str(row[5])))  # 归还日期
			self.tableWidget.setItem(i, 6, QTableWidgetItem(''))  # 是否逾期
			self.tableWidget.setItem(i, 7, QTableWidgetItem(''))  # 已归还时不显示按钮
			
			if row[5] is None:  
				# 未归还，添加归还按钮
				return_buttons = self.__dict__
				return_buttons['return_button_' + str(i)] = QPushButton('归还')
				self.tableWidget.setCellWidget(i, 7, return_buttons['return_button_' + str(i)])  # 假设你想在第8列（索引为7）添加按钮
				return_buttons['return_button_' + str(i)].clicked.connect(self.return_book)
				# 计算是否逾期
				borrow_date = row[4]
				borrow_date = datetime.strptime(f"{row[4].year}-{row[4].month}-{row[4].day}", '%Y-%m-%d')
				diff = (today - borrow_date).days
				if diff > 30:
					self.tableWidget.setItem(i, 6, QTableWidgetItem('是'))
				else:
					self.tableWidget.setItem(i, 6, QTableWidgetItem('否'))
			
			i += 1

	def return_book(self):
		current_row = self.tableWidget.currentRow()
		bid = self.tableWidget.item(current_row, 0).text()
		borrow_date = self.tableWidget.item(current_row, 4).text()
		# 模拟触发器，以下为还一本书后引发的操作
		# 1.更改Book表中的bstatus
		self.query = f"update Book set bstatus=1 where bid ='{bid}';"
		success = self.execute(False)
		if success == False:
			self.error_input('还书失败！')
			return
		
		# 2.在Borrow表中更新return_Date
		self.query = f"update Borrow set return_Date='{str(today)[:10]}' where book_ID='{bid}' and borrow_Date='{str(borrow_date)}' and reader_ID = '{current_user[0][0]}';"
		self.execute(False)

		QMessageBox.information(self, "提示", "还书成功！", QMessageBox.Yes)
		# 重新显示搜索结果
		self.search_book(self.search_mode)
		
		
class ManagerWindow(QMainWindow, Ui_ManagerWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.bind_up()
	
	def bind_up(self):
		self.pushButton.clicked.connect(self.user_manage)
		self.pushButton_2.clicked.connect(self.add_book)
		self.pushButton_3.clicked.connect(self.clear_lineEdit)
		self.pushButton_4.clicked.connect(self.search_book)
	
	def execute(self, recieve):
		global db
		result = []
		if status == 0:
			cursor = db.cursor()
			try:
				cursor.execute(self.query)
			except:
				self.error_input('SQL执行失败')
				db.rollback()
				return False
			if recieve:
				result = cursor.fetchall()
			else:
				result = cursor.fetchall()
				if(len(result) == 0):	
					result = False
				else: result = True
			db.commit()
			cursor.close()

		self.last = '' #每进行一次操作需要刷新 doubleclicked item时记录的待更改值
		return result
	
	def error_input(self, err_msg):
		QMessageBox.information(self, "错误提示", err_msg, QMessageBox.Yes)

	def user_manage(self):
		self.tableWidget.setRowCount(0)
		self.query = 'select * from Reader;'
		user_info = self.execute(True)
		if len(user_info) == 0: 
			self.error_input("暂无用户！")
			return
		for row in user_info: 
			i = 0
			self.tableWidget.insertRow(i)  # 尾部插入一行
			self.tableWidget.setItem(i, 0, QTableWidgetItem(str(row[0])))
			self.tableWidget.setItem(i, 1, QTableWidgetItem(str(row[2])))
			self.tableWidget.setItem(i, 2, QTableWidgetItem(str(row[3])))
			self.tableWidget.setItem(i, 3, QTableWidgetItem(str(row[4])))
			self.query = "select getBorrowTimes('{}');".format(row[0])
			cnt = self.execute(True)
			self.tableWidget.setItem(i, 4, QTableWidgetItem(str(cnt[0][0])))

			return_button = QPushButton('删除用户')
			self.tableWidget.setCellWidget(i, 5, return_button)
			return_button.clicked.connect(self.delete_user)
			i += 1

	def delete_user(self):
		current_row = self.tableWidget.currentRow()
		rid = self.tableWidget.item(current_row, 0).text()
		rname = self.tableWidget.item(current_row, 1).text()
		self.query = "delete from Reader where rid='{}';".format(rid)
		if(self.execute(False)):
			QMessageBox.information(self, "提示", f"删除用户{rname}成功！", QMessageBox.Yes)
		# 释放该用户借的书
		self.query = f"update Book set bstatus = 1 where bid in (select book_ID from Borrow where reader_ID ='{rid}' and return_Date is NULL);"
		self.execute(False)
		# 修改归还日期为今天
		self.query = f"update Borrow set return_Date = {str(today.year)}-{str(today.month)}-{str(today.day)} where reader_ID ='{rid}' and return_Date is NULL;"
		self.user_manage()
	
	def add_book(self):
		bid = self.lineEdit.text()
		bname = self.lineEdit_2.text()
		author = self.lineEdit_3.text()
		price = self.lineEdit_4.text()
		if(bid == '' or bname == '' or author == '' or price == ''):
			self.error_input('输入信息不足！')
			return
		self.query = f"select * from Book where bid='{bid}';"
		tmp = self.execute(False)
		if tmp :
			self.error_input('书号已存在！请更改书号')
			return
		self.query = f"insert into Book(bid, bname, author, price) Values('{bid}', '{bname}', '{author}', '{price}');"
		self.execute(False)
		QMessageBox.information(self, "提示", f"书籍《{bname}》上架成功！", QMessageBox.Yes)

	def clear_lineEdit(self):
		self.lineEdit.clear()
		self.lineEdit_2.clear()
		self.lineEdit_3.clear()
		self.lineEdit_4.clear()
	
	def search_book(self):
		self.tableWidget_2.setRowCount(0)  # 清空表格上次搜索记录
		bid = self.lineEdit.text()
		bname = self.lineEdit_2.text()
		author = self.lineEdit_3.text()
		my_price = self.lineEdit_4.text()
		if my_price == '': 
			self.query = f"select * from Book where bid LIKE '%{bid}%' and bname LIKE '%{bname}%' and author LIKE '%{author}%';"
		else:
			self.query = f"select * from Book where bid LIKE '%{bid}%' and bname LIKE '%{bname}%' and author LIKE '%{author}%' and ABS({float(my_price)} - price) <= 0.0001;"
		book_info = self.execute(True)
		if len(book_info) == 0: 
			self.error_input("未找到相关书籍！")
			return
		for row in book_info: 
			i = 0
			bstatus = "可借" if row[4] else "不可借"
			self.tableWidget_2.insertRow(i)  # 尾部插入一行
			self.tableWidget_2.setItem(i, 0, QTableWidgetItem(str(row[0])))  # book_id
			self.tableWidget_2.setItem(i, 1, QTableWidgetItem(str(row[1])))  # 书名
			self.tableWidget_2.setItem(i, 2, QTableWidgetItem(str(row[2])))  # 作者
			self.tableWidget_2.setItem(i, 3, QTableWidgetItem(str(row[3])))  # 价格
			self.tableWidget_2.setItem(i, 4, QTableWidgetItem(bstatus))  # 图书状态
			self.tableWidget_2.setItem(i, 5, QTableWidgetItem(str(row[5])))  # 借阅次数
			if row[4]: 
				delete_buttons = self.__dict__
				delete_buttons['delete_button_' + str(i)] = QPushButton('下架')
				self.tableWidget_2.setCellWidget(i, 6, delete_buttons['delete_button_' + str(i)])  # 假设你想在第8列（索引为7）添加按钮
				delete_buttons['delete_button_' + str(i)].clicked.connect(self.delete_book)
			i += 1

	def delete_book(self):
		current_row = self.tableWidget.currentRow()
		bid = self.tableWidget.item(current_row, 0).text()
		self.query = "delete from Book where bid='{}';".format(bid)
		self.execute(False)


class WelcomeWindow(QMainWindow, Ui_WelcomeWindow):
	def __init__(self, TestWindow, PersonalnformationWindow, BorrowWindow, ReturnWindow, ManagerWindow):
		super().__init__()
		# 定义接下来要跳转的窗口
		self.PersonalnformationWindow = PersonalnformationWindow
		self.BorrowWindow = BorrowWindow
		self.ReturnWindow = ReturnWindow
		self.ManagerWindow = ManagerWindow
		self.TestWindow = TestWindow

		self.setupUi(self)
		self.bind_up()
		
	def bind_up(self):
		self.pushButton_1.clicked.connect(lambda: self.PersonalnformationWindow.show())
		self.pushButton_2.clicked.connect(lambda: self.BorrowWindow.show())
		self.pushButton_3.clicked.connect(lambda: self.ReturnWindow.show())
		self.pushButton_4.clicked.connect(lambda: self.ManagerWindow.show())
	
	def execute(self, recieve):
		global db
		result = []
		if status == 0:
			cursor = db.cursor()
			try: 
				cursor.execute(self.query)
			except:
				self.error_input('SQL执行失败')
				db.rollback()
				return False
			if recieve:
				result = cursor.fetchall()
			else:
				result = cursor.fetchall()
				if(len(result) == 0): 
					result = False
				else: result = True
			db.commit()
			cursor.close()
		self.last = '' #每进行一次操作需要刷新 doubleclicked item时记录的待更改值
		return result

	def error_input(self, err_msg):
		QMessageBox.information(self, "错误提示", err_msg, QMessageBox.Yes)


if __name__ == "__main__":
	global db
	try:
		db = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='Fsk20030422',db="library", charset='utf8')
		print("Connected successfully!")
		status = 0
	except:
		status = 1
		print("Failed to connect the database!")

	app = QtWidgets.QApplication(sys.argv)

	LoginWindow = LoginWindow()
	TestWindow = TestWindow()
	PersonnalInformationWindow = PersonnalInformationWindow()
	BorrowWindow = BorrowWindow()
	ReturnWindow = ReturnWindow()
	ManagerWindow = ManagerWindow()

	welcome_window = WelcomeWindow(TestWindow, PersonnalInformationWindow, BorrowWindow, ReturnWindow, ManagerWindow)
	LoginWindow.welcome_window = welcome_window
	LoginWindow.show()

	sys.exit(app.exec_())
	
		