# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'borrow.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BorrowWindow(object):
    def setupUi(self, BorrowWindow):
        BorrowWindow.setObjectName("BorrowWindow")
        BorrowWindow.resize(1400, 800)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(16)
        BorrowWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(BorrowWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 100, 231, 41))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(330, 100, 641, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1000, 100, 141, 41))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(170, 255, 255);\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(80, 170, 1231, 391))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(6, item)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1160, 100, 151, 41))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(16)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 85, 127);\n"
"")
        self.pushButton_2.setObjectName("pushButton_2")
        BorrowWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(BorrowWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 18))
        self.menubar.setObjectName("menubar")
        BorrowWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(BorrowWindow)
        self.statusbar.setObjectName("statusbar")
        BorrowWindow.setStatusBar(self.statusbar)

        self.retranslateUi(BorrowWindow)
        QtCore.QMetaObject.connectSlotsByName(BorrowWindow)

    def retranslateUi(self, BorrowWindow):
        _translate = QtCore.QCoreApplication.translate
        BorrowWindow.setWindowTitle(_translate("BorrowWindow", "书目检索"))
        self.label.setText(_translate("BorrowWindow", "输入任意词检索"))
        self.pushButton.setText(_translate("BorrowWindow", "搜索"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("BorrowWindow", "书号"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("BorrowWindow", "书名"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("BorrowWindow", "作者"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("BorrowWindow", "价格"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("BorrowWindow", "图书状态"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("BorrowWindow", "借阅次数"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("BorrowWindow", "点击借阅"))
        self.pushButton_2.setText(_translate("BorrowWindow", "清空输入"))
