# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Qt_Designer_LoadDialogWithAirCraftsAxXhku.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1025, 375)
        self.label_12 = QLabel(Dialog)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(940, 230, 81, 20))
        self.lineEdit_DSN_FN = QLineEdit(Dialog)
        self.lineEdit_DSN_FN.setObjectName(u"lineEdit_DSN_FN")
        self.lineEdit_DSN_FN.setGeometry(QRect(520, 320, 201, 20))
        self.lineEdit_ODBCversion_FN = QLineEdit(Dialog)
        self.lineEdit_ODBCversion_FN.setObjectName(u"lineEdit_ODBCversion_FN")
        self.lineEdit_ODBCversion_FN.setGeometry(QRect(520, 260, 201, 20))
        self.label_16 = QLabel(Dialog)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(530, 80, 181, 16))
        self.label_11 = QLabel(Dialog)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(150, 40, 251, 20))
        self.label_11.setLayoutDirection(Qt.LeftToRight)
        self.comboBox_DSN_FN = QComboBox(Dialog)
        self.comboBox_DSN_FN.setObjectName(u"comboBox_DSN_FN")
        self.comboBox_DSN_FN.setGeometry(QRect(520, 140, 201, 22))
        self.label_9 = QLabel(Dialog)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(530, 120, 181, 16))
        self.pushButton_Connect_FN = QPushButton(Dialog)
        self.pushButton_Connect_FN.setObjectName(u"pushButton_Connect_FN")
        self.pushButton_Connect_FN.setGeometry(QRect(540, 170, 181, 23))
        self.lineEdit_Driver_FN = QLineEdit(Dialog)
        self.lineEdit_Driver_FN.setObjectName(u"lineEdit_Driver_FN")
        self.lineEdit_Driver_FN.setGeometry(QRect(520, 230, 201, 20))
        self.lineEdit_Schema_FN = QLineEdit(Dialog)
        self.lineEdit_Schema_FN.setObjectName(u"lineEdit_Schema_FN")
        self.lineEdit_Schema_FN.setGeometry(QRect(520, 290, 201, 20))
        self.label_14 = QLabel(Dialog)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(940, 260, 81, 20))
        self.comboBox_DB_FN = QComboBox(Dialog)
        self.comboBox_DB_FN.setObjectName(u"comboBox_DB_FN")
        self.comboBox_DB_FN.setGeometry(QRect(520, 60, 201, 22))
        self.comboBox_Driver_FN = QComboBox(Dialog)
        self.comboBox_Driver_FN.setObjectName(u"comboBox_Driver_FN")
        self.comboBox_Driver_FN.setGeometry(QRect(520, 100, 201, 22))
        self.label_8 = QLabel(Dialog)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(530, 40, 221, 20))
        self.label_15 = QLabel(Dialog)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(940, 290, 81, 20))
        self.pushButton_Disconnect_FN = QPushButton(Dialog)
        self.pushButton_Disconnect_FN.setObjectName(u"pushButton_Disconnect_FN")
        self.pushButton_Disconnect_FN.setGeometry(QRect(540, 200, 181, 23))
        self.pushButton_GetStarted = QPushButton(Dialog)
        self.pushButton_GetStarted.setObjectName(u"pushButton_GetStarted")
        self.pushButton_GetStarted.setGeometry(QRect(840, 350, 111, 21))
        self.pushButton_ChooseTXTFile = QPushButton(Dialog)
        self.pushButton_ChooseTXTFile.setObjectName(u"pushButton_ChooseTXTFile")
        self.pushButton_ChooseTXTFile.setGeometry(QRect(40, 350, 91, 23))
        self.lineEdit_TXTFile = QLineEdit(Dialog)
        self.lineEdit_TXTFile.setObjectName(u"lineEdit_TXTFile")
        self.lineEdit_TXTFile.setGeometry(QRect(140, 350, 371, 20))
        self.lineEdit_TXTFile.setReadOnly(False)
        self.lineEdit_CSVFile = QLineEdit(Dialog)
        self.lineEdit_CSVFile.setObjectName(u"lineEdit_CSVFile")
        self.lineEdit_CSVFile.setGeometry(QRect(140, 320, 371, 20))
        self.lineEdit_CSVFile.setReadOnly(False)
        self.pushButton_ChooseCSVFile = QPushButton(Dialog)
        self.pushButton_ChooseCSVFile.setObjectName(u"pushButton_ChooseCSVFile")
        self.pushButton_ChooseCSVFile.setGeometry(QRect(40, 320, 91, 23))
        self.comboBox_Driver_RT = QComboBox(Dialog)
        self.comboBox_Driver_RT.setObjectName(u"comboBox_Driver_RT")
        self.comboBox_Driver_RT.setGeometry(QRect(320, 140, 191, 22))
        self.label_18 = QLabel(Dialog)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(330, 80, 171, 20))
        self.comboBox_DB_RT = QComboBox(Dialog)
        self.comboBox_DB_RT.setObjectName(u"comboBox_DB_RT")
        self.comboBox_DB_RT.setGeometry(QRect(320, 100, 191, 22))
        self.label_19 = QLabel(Dialog)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(330, 120, 111, 16))
        self.lineEdit_ODBCversion_RT = QLineEdit(Dialog)
        self.lineEdit_ODBCversion_RT.setObjectName(u"lineEdit_ODBCversion_RT")
        self.lineEdit_ODBCversion_RT.setGeometry(QRect(320, 260, 191, 20))
        self.lineEdit_Driver_RT = QLineEdit(Dialog)
        self.lineEdit_Driver_RT.setObjectName(u"lineEdit_Driver_RT")
        self.lineEdit_Driver_RT.setGeometry(QRect(320, 230, 191, 20))
        self.lineEdit_Schema_RT = QLineEdit(Dialog)
        self.lineEdit_Schema_RT.setObjectName(u"lineEdit_Schema_RT")
        self.lineEdit_Schema_RT.setGeometry(QRect(320, 290, 191, 20))
        self.pushButton_Disconnect_RT = QPushButton(Dialog)
        self.pushButton_Disconnect_RT.setObjectName(u"pushButton_Disconnect_RT")
        self.pushButton_Disconnect_RT.setGeometry(QRect(380, 200, 131, 23))
        self.pushButton_Connect_RT = QPushButton(Dialog)
        self.pushButton_Connect_RT.setObjectName(u"pushButton_Connect_RT")
        self.pushButton_Connect_RT.setGeometry(QRect(380, 170, 131, 23))
        self.label_25 = QLabel(Dialog)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QRect(10, 20, 121, 121))
        self.label_25.setPixmap(QPixmap(u"\u0417\u043d\u0430\u0447\u043a\u0438 (\u0418\u043a\u043e\u043d\u043a\u0438)/2059278.png"))
        self.lineEdit_Schema_AL = QLineEdit(Dialog)
        self.lineEdit_Schema_AL.setObjectName(u"lineEdit_Schema_AL")
        self.lineEdit_Schema_AL.setGeometry(QRect(140, 290, 171, 20))
        self.lineEdit_Driver_AL = QLineEdit(Dialog)
        self.lineEdit_Driver_AL.setObjectName(u"lineEdit_Driver_AL")
        self.lineEdit_Driver_AL.setGeometry(QRect(140, 230, 171, 20))
        self.lineEdit_ODBCversion_AL = QLineEdit(Dialog)
        self.lineEdit_ODBCversion_AL.setObjectName(u"lineEdit_ODBCversion_AL")
        self.lineEdit_ODBCversion_AL.setGeometry(QRect(140, 260, 171, 20))
        self.comboBox_DB_AL = QComboBox(Dialog)
        self.comboBox_DB_AL.setObjectName(u"comboBox_DB_AL")
        self.comboBox_DB_AL.setGeometry(QRect(140, 100, 171, 22))
        self.label_20 = QLabel(Dialog)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(150, 120, 111, 20))
        self.pushButton_Disconnect_AL = QPushButton(Dialog)
        self.pushButton_Disconnect_AL.setObjectName(u"pushButton_Disconnect_AL")
        self.pushButton_Disconnect_AL.setGeometry(QRect(170, 200, 141, 23))
        self.comboBox_Driver_AL = QComboBox(Dialog)
        self.comboBox_Driver_AL.setObjectName(u"comboBox_Driver_AL")
        self.comboBox_Driver_AL.setGeometry(QRect(140, 140, 171, 22))
        self.pushButton_Connect_AL = QPushButton(Dialog)
        self.pushButton_Connect_AL.setObjectName(u"pushButton_Connect_AL")
        self.pushButton_Connect_AL.setGeometry(QRect(170, 170, 141, 23))
        self.lineEdit_Server = QLineEdit(Dialog)
        self.lineEdit_Server.setObjectName(u"lineEdit_Server")
        self.lineEdit_Server.setGeometry(QRect(140, 60, 371, 20))
        self.label_21 = QLabel(Dialog)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QRect(150, 80, 141, 20))
        self.label_28 = QLabel(Dialog)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setGeometry(QRect(20, 180, 41, 41))
        self.label_28.setPixmap(QPixmap(u"\u0417\u043d\u0430\u0447\u043a\u0438 (\u0418\u043a\u043e\u043d\u043a\u0438)/a_22.ico"))
        self.label_29 = QLabel(Dialog)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setGeometry(QRect(70, 180, 41, 41))
        self.label_29.setPixmap(QPixmap(u"\u0417\u043d\u0430\u0447\u043a\u0438 (\u0418\u043a\u043e\u043d\u043a\u0438)/a_23.ico"))
        self.dateEdit_BeginDate = QDateEdit(Dialog)
        self.dateEdit_BeginDate.setObjectName(u"dateEdit_BeginDate")
        self.dateEdit_BeginDate.setGeometry(QRect(520, 350, 110, 22))
        self.label_30 = QLabel(Dialog)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setGeometry(QRect(120, 180, 41, 41))
        self.label_30.setPixmap(QPixmap(u"\u0417\u043d\u0430\u0447\u043a\u0438 (\u0418\u043a\u043e\u043d\u043a\u0438)/a_21.ico"))
        self.checkBox_SetInputDate = QCheckBox(Dialog)
        self.checkBox_SetInputDate.setObjectName(u"checkBox_SetInputDate")
        self.checkBox_SetInputDate.setGeometry(QRect(640, 350, 191, 18))
        self.label_10 = QLabel(Dialog)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(940, 320, 61, 20))
        self.label_10.setLayoutDirection(Qt.RightToLeft)
        self.label_Version = QLabel(Dialog)
        self.label_Version.setObjectName(u"label_Version")
        self.label_Version.setGeometry(QRect(10, 290, 121, 20))
        self.label_Version.setLayoutDirection(Qt.LeftToRight)
        self.pushButton_Disconnect_AC = QPushButton(Dialog)
        self.pushButton_Disconnect_AC.setObjectName(u"pushButton_Disconnect_AC")
        self.pushButton_Disconnect_AC.setGeometry(QRect(880, 200, 131, 23))
        self.label_13 = QLabel(Dialog)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(820, 120, 181, 16))
        self.pushButton_Connect_AC = QPushButton(Dialog)
        self.pushButton_Connect_AC.setObjectName(u"pushButton_Connect_AC")
        self.pushButton_Connect_AC.setGeometry(QRect(880, 170, 131, 23))
        self.comboBox_DSN_AC = QComboBox(Dialog)
        self.comboBox_DSN_AC.setObjectName(u"comboBox_DSN_AC")
        self.comboBox_DSN_AC.setGeometry(QRect(810, 140, 201, 22))
        self.lineEdit_DSN_AC = QLineEdit(Dialog)
        self.lineEdit_DSN_AC.setObjectName(u"lineEdit_DSN_AC")
        self.lineEdit_DSN_AC.setGeometry(QRect(730, 320, 201, 20))
        self.lineEdit_Schema_AC = QLineEdit(Dialog)
        self.lineEdit_Schema_AC.setObjectName(u"lineEdit_Schema_AC")
        self.lineEdit_Schema_AC.setGeometry(QRect(730, 290, 201, 20))
        self.lineEdit_Driver_AC = QLineEdit(Dialog)
        self.lineEdit_Driver_AC.setObjectName(u"lineEdit_Driver_AC")
        self.lineEdit_Driver_AC.setGeometry(QRect(730, 230, 201, 20))
        self.lineEdit_ODBCversion_AC = QLineEdit(Dialog)
        self.lineEdit_ODBCversion_AC.setObjectName(u"lineEdit_ODBCversion_AC")
        self.lineEdit_ODBCversion_AC.setGeometry(QRect(730, 260, 201, 20))
        self.lineEdit_Server_remote = QLineEdit(Dialog)
        self.lineEdit_Server_remote.setObjectName(u"lineEdit_Server_remote")
        self.lineEdit_Server_remote.setGeometry(QRect(140, 20, 371, 20))
        self.label_17 = QLabel(Dialog)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(150, 0, 261, 20))
        self.label_17.setLayoutDirection(Qt.LeftToRight)
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(750, 9, 171, 81))
        self.radioButton_DSN = QRadioButton(self.groupBox)
        self.radioButton_DSN.setObjectName(u"radioButton_DSN")
        self.radioButton_DSN.setGeometry(QRect(10, 50, 41, 18))
        self.radioButton_DB = QRadioButton(self.groupBox)
        self.radioButton_DB.setObjectName(u"radioButton_DB")
        self.radioButton_DB.setGeometry(QRect(10, 20, 151, 18))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"\u0414\u0440\u0430\u0439\u0432\u0435\u0440 \u0421\u0423\u0411\u0414", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"\u0414\u0440\u0430\u0439\u0432\u0435\u0440 \u0421\u0423\u0411\u0414", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"\u0421\u0435\u0440\u0432\u0435\u0440 \u0421\u0423\u0411\u0414 \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u043e\u0432", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"DSN \u0430\u0432\u0438\u0430\u043f\u0435\u0440\u0435\u043b\u0435\u0442\u043e\u0432", None))
        self.pushButton_Connect_FN.setText(QCoreApplication.translate("Dialog", u"\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043a \u0411\u0414 \u0438\u043b\u0438 \u043a DSN", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"\u0412\u0435\u0440\u0441\u0438\u044f ODBC", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"\u041e\u043f\u0435\u0440\u0430\u0442\u0438\u0432\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435 \u043f\u043e \u0430\u0432\u0438\u0430\u043f\u0435\u0440\u0435\u043b\u0435\u0442\u0430\u043c", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"\u0421\u0445\u0435\u043c\u0430", None))
        self.pushButton_Disconnect_FN.setText(QCoreApplication.translate("Dialog", u"\u041e\u0442\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043e\u0442 \u0411\u0414 \u0438\u043b\u0438 \u043e\u0442 DSN", None))
        self.pushButton_GetStarted.setText(QCoreApplication.translate("Dialog", u"\u041d\u0430\u0447\u0430\u0442\u044c\u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0443", None))
        self.pushButton_ChooseTXTFile.setText(QCoreApplication.translate("Dialog", u"\u0424\u0430\u0439\u043b \u0436\u0443\u0440\u043d\u0430\u043b\u0430", None))
        self.pushButton_ChooseCSVFile.setText(QCoreApplication.translate("Dialog", u"\u0424\u0430\u0439\u043b \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"\u0421\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a \u0430\u044d\u0440\u043e\u043f\u043e\u0440\u0442\u043e\u0432", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"\u0414\u0440\u0430\u0439\u0432\u0435\u0440 \u0421\u0423\u0411\u0414", None))
        self.pushButton_Disconnect_RT.setText(QCoreApplication.translate("Dialog", u"\u041e\u0442\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043e\u0442 \u0411\u0414", None))
        self.pushButton_Connect_RT.setText(QCoreApplication.translate("Dialog", u"\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043a \u0411\u0414", None))
        self.label_25.setText("")
        self.label_20.setText(QCoreApplication.translate("Dialog", u"\u0414\u0440\u0430\u0439\u0432\u0435\u0440 \u0421\u0423\u0411\u0414", None))
        self.pushButton_Disconnect_AL.setText(QCoreApplication.translate("Dialog", u"\u041e\u0442\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043e\u0442 \u0411\u0414", None))
        self.pushButton_Connect_AL.setText(QCoreApplication.translate("Dialog", u"\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043a \u0411\u0414", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"\u0421\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a \u0430\u0432\u0438\u0430\u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0439", None))
        self.label_28.setText("")
        self.label_29.setText("")
        self.label_30.setText("")
        self.checkBox_SetInputDate.setText(QCoreApplication.translate("Dialog", u"\u041f\u0435\u0440\u0435\u043d\u043e\u0441 \u0434\u0430\u0442\u044b \u0438\u0437 \u0444\u0430\u0439\u043b\u0430 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"DSN-\u044b", None))
        self.label_Version.setText(QCoreApplication.translate("Dialog", u"\u0412\u0435\u0440\u0441\u0438\u044f \u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0438", None))
        self.pushButton_Disconnect_AC.setText(QCoreApplication.translate("Dialog", u"\u041e\u0442\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043e\u0442 DSN", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"\u0421\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a \u043f\u043e \u0441\u0430\u043c\u043e\u043b\u0435\u0442\u0430\u043c", None))
        self.pushButton_Connect_AC.setText(QCoreApplication.translate("Dialog", u"\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043a DSN", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"\u0421\u0435\u0440\u0432\u0435\u0440 \u0421\u0423\u0411\u0414 \u043e\u043f\u0435\u0440\u0430\u0442\u0438\u0432\u043d\u044b\u0445 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.radioButton_DSN.setText(QCoreApplication.translate("Dialog", u"DSN", None))
        self.radioButton_DB.setText(QCoreApplication.translate("Dialog", u"\u0411\u0430\u0437\u0430 \u0434\u0430\u043d\u043d\u044b\u0445 \u0438 \u0414\u0440\u0430\u0439\u0432\u0435\u0440", None))
    # retranslateUi
