#  Interpreter 3.7 -> 3.10


import pyodbc
import pandas
import itertools
import datetime
import time
import os
import sys
import socket
import threading
from xml.etree import ElementTree

# QtCore, QtGui, QtNetwork, QtOpenGL, QtScript, QtSQL (медленнее чем pyodbc), QtDesigner - запускаем в командной строке, QtXml (устарел) -> замена QXmlStreamReader, QXmlStreamWriter
from PyQt5 import QtWidgets  # оставил 5-ую версию (много наработок еще завязаны на нее)
import pathlib
import colorama
import termcolor

# Импорт модуля библиотек индивидуальной разработки
from modulesFilesWithClasses.moduleClasses import AirLine, AirCraft, AirPort, ServerNames, FileNames, Flags, States, ModifyFlight
from modulesFilesWithClasses.moduleClassesUIsSources import Ui_DialogLoadAirFlightsWithAirCrafts
# todo  - Сделать пользовательскую наработку (не библиотеку и не пакет) отдельным репозиторием
#       - Импортировать ее как подмодуль для повторного применения синхронно (mutualy connected) или асинхронно (independent) -> Импортировал асинхронно, обновление только вручную на командах git, для синхронного нет функционала
#       - Результат импорта -> на github-е - синяя неактивная ссылка, по которой никуда не перейдешь, внутри pyCharm-а - дубликат репозитория подмодуля в локальную ветку
# fixme pyCharm как графическая оболочка пока не работает с подмодулями в графическом режиме [@Aleks10](https://qna.habr.com/q/196071), а пока только командами 'git submodules'


myOwnDevelopingVersion = 8.7  # Версия. todo Пакеты на GitHub-е *.tar.gz (под Linux или под BSD) не нужны

colorama.init(autoreset=False)  # используем Colorama и Termcolor на Windows, оставляем цветовое оформление до следующего явного указания
print(termcolor.colored("Обработка v" + str(myOwnDevelopingVersion) + " загрузки рабочих данных в БД SQL Server-а", 'blue', 'on_yellow'))
print("Разработал Тарасов Сергей tsv19su@yandex.ru")
print(termcolor.colored("Пользователь = " + str(os.getlogin()), 'green', 'on_yellow'))


# Добавляем функционал


# Делаем свои рабочие экземпляры
A = AirLine()
C = AirCraft()
P = AirPort()
S = ServerNames()
F = FileNames()
Fl = Flags()
St = States()
#MF = ModifyFlight()


def myApplication():
    # Одно прикладное приложение
    myApp = QtWidgets.QApplication(sys.argv)
    # Делаем свой рабочий экземпляр
    myDialog = Ui_DialogLoadAirFlightsWithAirCrafts()
    myDialog.setupUi(Dialog=myDialog)  # надо вызывать явно
    myDialog.setFixedSize(940, 375)
    myDialog.setWindowTitle('Загрузка рабочих данных')
    # Дополняем функционал экземпляра главного диалога
    # Переводим в исходное состояние
    myDialog.label_Version.setText("Версия обработки " + str(myOwnDevelopingVersion))
    # Получаем список DSN-ов
    # Добавляем атрибут DSNs по ходу действия
    S.DSNs = A.getDataSources()  # добавленные системные DSN-ы
    if S.DSNs:
        for DSN in S.DSNs:
            if not DSN:
                break
            myDialog.comboBox_DSN_FN.addItem(str(DSN))
            myDialog.comboBox_DSN_AC.addItem(str(DSN))
    # Получаем список драйверов баз данных
    # Добавляем атрибут DriversODBC по ходу действия
    S.DriversODBC = A.getSQLDrivers()
    if S.DriversODBC:
        for DriverODBC in S.DriversODBC:
            if not DriverODBC:
                break
            myDialog.comboBox_Driver_AL.addItem(str(DriverODBC))
            myDialog.comboBox_Driver_RT.addItem(str(DriverODBC))
            myDialog.comboBox_Driver_FN.addItem(str(DriverODBC))
    # Добавляем базы данных в выпадающие списки
    myDialog.comboBox_DB_AL.addItem("AirLinesDBNew62")
    myDialog.comboBox_DB_RT.addItem("AirPortsAndRoutesDBNew62")
    myDialog.comboBox_DB_FN.addItem("AirFlightsDBNew42")
    myDialog.comboBox_DB_FN.addItem("AirFlightsDBNew52")
    myDialog.comboBox_DB_FN.addItem("AirFlightsDBNew62WorkBase")
    myDialog.comboBox_DB_FN.addItem("AirFlightsDBNew72WorkBase")
    myDialog.dateEdit_BeginDate.setToolTip("Дата начала периода загрузки рабочих данных")
    myDialog.checkBox_SetInputDate.setToolTip("Перенос даты авиарейса из входных данных")
    myDialog.pushButton_GetStarted.setToolTip("Запуск загрузки исходных данных по авиаперелетам \nВнимательно проверьте параметры загрузки")
    myDialog.radioButton_DSN_AirCrafts_DOM.setToolTip("При использовании ПОЛНОЙ модели восстановления БД\n данный метод мягко говоря сильно загружает файл журнала *.ldf")
    myDialog.radioButton_DSN_AirCrafts_SAX.setToolTip("Можно выставить в свойствах БД модель восстановления - ПОЛНАЯ \n экономит ресурсы, но работает медленнее")
    myDialog.radioButton_DB_AirFlights.setChecked(True)
    myDialog.radioButton_DSN_AirCrafts_DOM.setChecked(True)

    def PrepareForInputData(Key):
        myDialog.pushButton_ChooseCSVFile.setEnabled(Key)
        myDialog.lineEdit_CSVFile.setEnabled(Key)
        myDialog.pushButton_ChooseTXTFile.setEnabled(Key)
        myDialog.lineEdit_TXTFile.setEnabled(Key)
        myDialog.dateEdit_BeginDate.setEnabled(Key)
        if Key:
            myDialog.dateEdit_BeginDate.setCalendarPopup(True)
        myDialog.checkBox_SetInputDate.setEnabled(Key)
        myDialog.pushButton_GetStarted.setEnabled(Key)

    def UpdateAirLinesSourcesChoiceByStatesAndFlags():
        if St.Connected_AL:
            # Переключаем в рабочее состояние
            myDialog.comboBox_DB_AL.setEnabled(False)
            myDialog.comboBox_Driver_AL.setEnabled(False)
            if St.Connected_RT and (St.Connected_ACFN or St.Connected_AC_XML):
                PrepareForInputData(True)
        else:
            # Переключаем в исходное состояние
            if not St.Connected_RT:
                myDialog.lineEdit_Server.setEnabled(False)
            myDialog.lineEdit_Driver_AL.setEnabled(False)
            myDialog.lineEdit_ODBCversion_AL.setEnabled(False)
            myDialog.lineEdit_Schema_AL.setEnabled(False)
            myDialog.comboBox_DB_AL.setEnabled(True)
            myDialog.comboBox_Driver_AL.setEnabled(True)
            PrepareForInputData(False)

    def UpdateAirPortsSourcesChoiceByStatesAndFlags():
        if St.Connected_RT:
            # Переключаем в рабочее состояние
            myDialog.comboBox_DB_RT.setEnabled(False)
            myDialog.comboBox_Driver_RT.setEnabled(False)
            if St.Connected_AL and (St.Connected_ACFN or St.Connected_AC_XML):
                PrepareForInputData(True)
        else:
            # Переключаем в исходное состояние
            if not St.Connected_AL:
                myDialog.lineEdit_Server.setEnabled(False)
            myDialog.lineEdit_Driver_RT.setEnabled(False)
            myDialog.lineEdit_ODBCversion_RT.setEnabled(False)
            myDialog.lineEdit_Schema_RT.setEnabled(False)
            myDialog.comboBox_DB_RT.setEnabled(True)
            myDialog.comboBox_Driver_RT.setEnabled(True)
            PrepareForInputData(False)

    def UpdateFlightsSourcesChoiceByStatesAndFlags():
        # Состояния + Флаги -> Графическая оболочка
        if St.Connected_AC_XML or St.Connected_ACFN:
            # Переключаем в рабочее состояние
            myDialog.comboBox_DB_FN.setEnabled(False)
            myDialog.comboBox_Driver_FN.setEnabled(False)
            myDialog.comboBox_DSN_FN.setEnabled(False)
            myDialog.comboBox_DSN_AC.setEnabled(False)
            myDialog.groupBox.setEnabled(False)
            myDialog.groupBox_2.setEnabled(False)
            if St.Connected_AL and St.Connected_RT:
                PrepareForInputData(True)
        else:
            # Переключаем в исходное состояние
            myDialog.lineEdit_Server_remote.setEnabled(False)
            myDialog.lineEdit_Driver_AC.setEnabled(False)
            myDialog.lineEdit_ODBCversion_AC.setEnabled(False)
            myDialog.lineEdit_Schema_AC.setEnabled(False)
            myDialog.lineEdit_DSN_AC.setEnabled(False)
            myDialog.groupBox.setEnabled(True)
            if Fl.useAirCraftsDSN:
                myDialog.comboBox_DB_FN.setEnabled(False)
                myDialog.comboBox_Driver_FN.setEnabled(False)
                myDialog.comboBox_DSN_FN.setEnabled(False)
                myDialog.comboBox_DSN_AC.setEnabled(True)
                myDialog.groupBox_2.setEnabled(True)
            else:
                myDialog.comboBox_DSN_AC.setEnabled(False)
                myDialog.groupBox_2.setEnabled(False)
                if Fl.useAirFlightsDB:
                    myDialog.comboBox_DB_FN.setEnabled(True)
                    myDialog.comboBox_Driver_FN.setEnabled(True)
                    myDialog.comboBox_DSN_FN.setEnabled(False)
                else:
                    myDialog.comboBox_DB_FN.setEnabled(False)
                    myDialog.comboBox_Driver_FN.setEnabled(False)
                    myDialog.comboBox_DSN_FN.setEnabled(True)
            # Переключаем в исходное состояние
            PrepareForInputData(False)

    def RadioButtonsToggled():
        # Переключатели -> Флаги
        if myDialog.radioButton_DSN_AirCrafts.isChecked():
            Fl.useAirCraftsDSN = True
        else:
            Fl.useAirCraftsDSN = False
            if myDialog.radioButton_DB_AirFlights.isChecked():
                Fl.useAirFlightsDB = True
            if myDialog.radioButton_DSN_AirFlights.isChecked():
                Fl.useAirFlightsDB = False
        UpdateFlightsSourcesChoiceByStatesAndFlags()

    def RadioButtonsXQueryToggled():
        if myDialog.radioButton_DSN_AirCrafts_DOM.isChecked():
            Fl.useXQuery = False
        if myDialog.radioButton_DSN_AirCrafts_SAX.isChecked():
            Fl.useXQuery = True

    UpdateAirLinesSourcesChoiceByStatesAndFlags()
    UpdateAirPortsSourcesChoiceByStatesAndFlags()
    RadioButtonsToggled()
    RadioButtonsXQueryToggled()
    UpdateFlightsSourcesChoiceByStatesAndFlags()
    myDialog.pushButton_Disconnect_AL.setEnabled(False)
    myDialog.pushButton_Disconnect_RT.setEnabled(False)
    myDialog.pushButton_Disconnect_AC.setEnabled(False)
    myDialog.pushButton_GetStarted.setEnabled(False)
    myDialog.label_execute.setEnabled(False)

    # Привязки обработчиков todo без lambda не работает
    myDialog.radioButton_DB_AirFlights.toggled.connect(lambda: RadioButtonsToggled())
    myDialog.radioButton_DSN_AirFlights.toggled.connect(lambda: RadioButtonsToggled())
    myDialog.radioButton_DSN_AirCrafts.toggled.connect(lambda: RadioButtonsToggled())
    myDialog.radioButton_DSN_AirCrafts_DOM.toggled.connect(lambda: RadioButtonsXQueryToggled())
    myDialog.radioButton_DSN_AirCrafts_SAX.toggled.connect(lambda: RadioButtonsXQueryToggled())
    #myDialog.groupBox.toggled.connect(lambda: RadioButtonsToggled())  # fixme не реагирует
    myDialog.pushButton_Connect_AL.clicked.connect(lambda: PushButtonConnect_AL())  # Подключиться к базе данных
    myDialog.pushButton_Disconnect_AL.clicked.connect(lambda: PushButtonDisconnect_AL())  # Отключиться от базы данных
    myDialog.pushButton_Connect_RT.clicked.connect(lambda: PushButtonConnect_RT())
    myDialog.pushButton_Disconnect_RT.clicked.connect(lambda: PushButtonDisconnect_RT())
    myDialog.pushButton_Connect_AC.clicked.connect(lambda: PushButtonConnect_ACFN())
    myDialog.pushButton_Disconnect_AC.clicked.connect(lambda: PushButtonDisconnect_ACFN())
    myDialog.pushButton_ChooseCSVFile.clicked.connect(lambda: PushButtonChooseCSVFile())  # Выбрать файл данных
    myDialog.pushButton_ChooseTXTFile.clicked.connect(lambda: PushButtonChooseTXTFile())  # Выбрать файл журнала
    myDialog.pushButton_GetStarted.clicked.connect(lambda: PushButtonGetStarted())  # Начать загрузку

    def PushButtonConnect_AL():
        myDialog.pushButton_Connect_AL.setEnabled(False)
        if not St.Connected_AL:
            # Подключаемся к базе данных авиакомпаний
            # todo Схема по умолчанию - dbo, другая схема указывается в явном виде
            # https://docs.microsoft.com/ru-ru/previous-versions/dotnet/framework/data/adonet/sql/ownership-and-user-schema-separation-in-sql-server
            ChoiceDB = myDialog.comboBox_DB_AL.currentText()
            ChoiceDriver = myDialog.comboBox_Driver_AL.currentText()
            # Добавляем атрибуты DataBase, DriverODBC
            S.DataBase_AL = str(ChoiceDB)
            S.DriverODBC_AL = str(ChoiceDriver)
            if A.connectDB_AL(S.DriverODBC_AL, S.ServerName, S.DataBase_AL):
                print("  БД = ", S.DataBase_AL, "подключена")
                Data = A.getSQLData()
                print(" Data = " + str(Data))
                St.Connected_AL = True
                # Переключаем в рабочее состояние
                # SQL Server
                myDialog.lineEdit_Server.setEnabled(True)
                myDialog.lineEdit_Server.setText(Data[0])
                # Драйвер
                myDialog.lineEdit_Driver_AL.setEnabled(True)
                myDialog.lineEdit_Driver_AL.setText(Data[1])
                # версия ODBC
                myDialog.lineEdit_ODBCversion_AL.setEnabled(True)
                myDialog.lineEdit_ODBCversion_AL.setText(Data[2])
                # Схема (если из-под другой учетки, то выводит имя учетки)
                myDialog.lineEdit_Schema_AL.setEnabled(True)
                myDialog.lineEdit_Schema_AL.setText(Data[4])
                # Переводим в рабочее состояние (продолжение)
                UpdateAirLinesSourcesChoiceByStatesAndFlags()
                myDialog.pushButton_Disconnect_AL.setEnabled(True)
            else:
                myDialog.pushButton_Connect_AL.setEnabled(True)
                message = QtWidgets.QMessageBox()
                message.setText("Нет подключения к базе данных авиакомпаний")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()

    def PushButtonDisconnect_AL():
        # Обработчик кнопки 'Отключиться от базы данных'
        myDialog.pushButton_Disconnect_AL.setEnabled(False)
        if St.Connected_AL:
            A.disconnectAL()
            St.Connected_AL = False
        # Переключаем в исходное состояние
        UpdateAirLinesSourcesChoiceByStatesAndFlags()
        myDialog.pushButton_Connect_AL.setEnabled(True)

    def PushButtonConnect_RT():
        myDialog.pushButton_Connect_RT.setEnabled(False)
        if not St.Connected_RT:
            # Подключаемся к базе данных аэропортов и маршрутов
            # todo Схема по умолчанию - dbo, другая схема указывается в явном виде
            ChoiceDB = myDialog.comboBox_DB_RT.currentText()
            ChoiceDriver = myDialog.comboBox_Driver_RT.currentText()
            # Добавляем атрибуты DataBase, DriverODBC
            S.DataBase_RT = str(ChoiceDB)
            S.DriverODBC_RT = str(ChoiceDriver)
            if P.connectDB_RT(S.DriverODBC_RT, S.ServerName, S.DataBase_RT):
                print("  БД = ", S.DataBase_RT, "подключена")
                Data = P.getSQLData()
                print(" Data = " + str(Data))
                St.Connected_RT = True
                # Переключаем в рабочее состояние
                # SQL Server
                myDialog.lineEdit_Server.setText(Data[0])
                myDialog.lineEdit_Server.setEnabled(True)
                # Драйвер
                myDialog.lineEdit_Driver_RT.setText(Data[1])
                myDialog.lineEdit_Driver_RT.setEnabled(True)
                # версия ODBC
                myDialog.lineEdit_ODBCversion_RT.setText(Data[2])
                myDialog.lineEdit_ODBCversion_RT.setEnabled(True)
                # Схема (если из-под другой учетки, то выводит имя учетки)
                myDialog.lineEdit_Schema_RT.setText(Data[4])
                myDialog.lineEdit_Schema_RT.setEnabled(True)
                # Переводим в рабочее состояние (продолжение)
                UpdateAirPortsSourcesChoiceByStatesAndFlags()
                myDialog.pushButton_Disconnect_RT.setEnabled(True)
            else:
                myDialog.pushButton_Connect_RT.setEnabled(True)
                message = QtWidgets.QMessageBox()
                message.setText("Нет подключения к базе данных аэропортов и маршрутов")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()

    def PushButtonDisconnect_RT():
        # Обработчик кнопки 'Отключиться от базы данных'
        myDialog.pushButton_Disconnect_RT.setEnabled(False)
        if St.Connected_RT:
            P.disconnectRT()
            St.Connected_RT = False
        # Переключаем в исходное состояние
        UpdateAirPortsSourcesChoiceByStatesAndFlags()
        myDialog.pushButton_Connect_RT.setEnabled(True)

    def PushButtonConnect_ACFN():
        if Fl.useAirCraftsDSN:
            myDialog.pushButton_Connect_AC.setEnabled(False)
            if not St.Connected_AC_XML:
                # Подключаемся к базе данных самолетов
                # todo Схема по умолчанию - dbo, другая схема указывается в явном виде
                ChoiceDSN_AC_XML = myDialog.comboBox_DSN_AC.currentText()
                # Добавляем атрибут myDSN
                S.myDSN_AC_XML = str(ChoiceDSN_AC_XML)
                if C.connectDSN_AC_XML(S.myDSN_AC_XML):
                    Data = C.getSQLData()
                    print(" Data = " + str(Data))
                    St.Connected_AC_XML = True
                    # Переключаем в рабочее состояние
                    # SQL Server
                    myDialog.lineEdit_Server_remote.setEnabled(True)
                    myDialog.lineEdit_Server_remote.setText(Data[0])
                    # Драйвер
                    myDialog.lineEdit_Driver_AC.setEnabled(True)
                    myDialog.lineEdit_Driver_AC.setText(Data[1])
                    # версия ODBC
                    myDialog.lineEdit_ODBCversion_AC.setEnabled(True)
                    myDialog.lineEdit_ODBCversion_AC.setText(Data[2])
                    # Схема (если из-под другой учетки, то выводит имя учетки)
                    myDialog.lineEdit_Schema_AC.setEnabled(True)
                    myDialog.lineEdit_Schema_AC.setText(Data[4])
                    # Источник данных
                    myDialog.lineEdit_DSN_AC.setEnabled(True)
                    myDialog.lineEdit_DSN_AC.setText(Data[3])
                    # Переводим в рабочее состояние (продолжение)
                    UpdateFlightsSourcesChoiceByStatesAndFlags()
                    myDialog.pushButton_Disconnect_AC.setEnabled(True)
                else:
                    myDialog.pushButton_Connect_AC.setEnabled(True)
                    message = QtWidgets.QMessageBox()
                    message.setText("Нет подключения к БД самолетов")
                    message.setIcon(QtWidgets.QMessageBox.Warning)
                    message.exec_()
        else:
            myDialog.pushButton_Connect_AC.setEnabled(False)
            if not St.Connected_ACFN:
                # Подключаемся к базе данных авиаперелетов
                # todo Схема по умолчанию - dbo, другая схема указывается в явном виде
                ChoiceDB_ACFN = myDialog.comboBox_DB_FN.currentText()
                ChoiceDriver_ACFN = myDialog.comboBox_Driver_FN.currentText()
                # Добавляем атрибуты DataBase, DriverODBC
                S.DataBase_ACFN = str(ChoiceDB_ACFN)
                S.DriverODBC_ACFN = str(ChoiceDriver_ACFN)
                ChoiceDSN_ACFN = myDialog.comboBox_DSN_FN.currentText()
                # Добавляем атрибут myDSN
                S.myDSN_ACFN = str(ChoiceDSN_ACFN)
                Connected_ACFN = False
                # Добавляем атрибут cnxn
                if Fl.useAirFlightsDB:
                    if C.connectDB_AC(S.DriverODBC_ACFN, S.ServerNameFlights, S.DataBase_ACFN) and C.connectDB_FN(S.DriverODBC_ACFN, S.ServerNameFlights, S.DataBase_ACFN):
                        St.Connected_ACFN = True
                else:
                    if C.connectDSN_AC(S.myDSN_ACFN) and C.connectDSN_FN(S.myDSN_ACFN):
                        St.Connected_ACFN = True
                if St.Connected_ACFN:
                    Data = C.getSQLData()
                    print(" Data = " + str(Data))
                    # Переключаем в рабочее состояние
                    # SQL Server
                    myDialog.lineEdit_Server_remote.setEnabled(True)
                    myDialog.lineEdit_Server_remote.setText(Data[0])
                    # Драйвер
                    myDialog.lineEdit_Driver_AC.setEnabled(True)
                    myDialog.lineEdit_Driver_AC.setText(Data[1])
                    # Версия ODBC
                    myDialog.lineEdit_ODBCversion_AC.setEnabled(True)
                    myDialog.lineEdit_ODBCversion_AC.setText(Data[2])
                    # Схема (если из-под другой учетки, то выводит имя учетки)
                    myDialog.lineEdit_Schema_AC.setEnabled(True)
                    myDialog.lineEdit_Schema_AC.setText(Data[4])
                    # Источник данных
                    myDialog.lineEdit_DSN_AC.setEnabled(True)
                    myDialog.lineEdit_DSN_AC.setText(Data[3])
                    # Переводим в рабочее состояние (продолжение)
                    UpdateFlightsSourcesChoiceByStatesAndFlags()
                    if St.Connected_AL and St.Connected_RT:
                        PrepareForInputData(True)
                    myDialog.pushButton_Disconnect_AC.setEnabled(True)
                else:
                    myDialog.pushButton_Connect_AC.setEnabled(True)
                    message = QtWidgets.QMessageBox()
                    message.setText("Нет подключения к БД авиаперелетов")
                    message.setIcon(QtWidgets.QMessageBox.Warning)
                    message.exec_()

    def PushButtonDisconnect_ACFN():
        # Обработчик кнопки 'Отключиться от базы данных'
        myDialog.pushButton_Disconnect_AC.setEnabled(False)
        if St.Connected_AC_XML:
            C.disconnectAC_XML()
            St.Connected_AC_XML = False
        if St.Connected_ACFN:
            C.disconnectAC()
            C.disconnectFN()
            St.Connected_AC = False
            St.Connected_ACFN = False
        UpdateFlightsSourcesChoiceByStatesAndFlags()
        myDialog.pushButton_Connect_AC.setEnabled(True)


    def PushButtonChooseCSVFile():
        filter = "Data files (*.csv)"
        F.InputFileCSV = QtWidgets.QFileDialog.getOpenFileName(None, "Открыть рабочие данные", ' ', filter=filter)[0]
        urnCSV = F.InputFileCSV.rstrip(os.sep)  # не сработало
        filenameCSV = pathlib.Path(F.InputFileCSV).name
        myDialog.lineEdit_CSVFile.setText(filenameCSV)

    def PushButtonChooseTXTFile():
        filter = "Log Files (*.txt *.text)"
        F.LogFileTXT = QtWidgets.QFileDialog.getOpenFileName(None, "Открыть журнал", ' ', filter=filter)[0]
        filenameTXT = pathlib.Path(F.LogFileTXT).name
        myDialog.lineEdit_TXTFile.setText(filenameTXT)

    def ModifyAirFlight(ac, al, fn, dep, arr, flightdate, begindate, useAirCrafts, useXQuery):

        class Results:
            Result = 0  # Коды возврата: 0 - несработка, 1 - вставили, 2 - сплюсовали

        db_air_route = P.QueryAirRoute(dep, arr).AirRouteUniqueNumber
        if db_air_route is not None:
            db_air_craft = C.QueryAirCraftByRegistration(ac, useAirCrafts).AirCraftUniqueNumber
            if db_air_craft is not None:
                if useAirCrafts:
                    if useXQuery:
                        try:
                            #SQLQuery = "DECLARE @ReturnData INT = 5 "
                            #SQLQuery += "SET @ReturnData = 5 "
                            #self.seekAC_XML.execute(SQLQuery)
                            # todo При отладке вставлять тестовый файлик. После отладки убрать из БД все тестовые строки и убрать из строки ниже "Test" ...
                            SQLQuery = "EXECUTE dbo.SPUpdateFlightsByRoutes '" + str(ac) + "', '" + str(al) + str(fn) + "Test" + "', " + str(db_air_route) + ", '" + str(flightdate) + "', '" + str(begindate) + "' "
                            C.seekAC_XML.execute(SQLQuery)
                            #SQLQuery = "SELECT @ReturnData "
                            #C.seekAC_XML.execute(SQLQuery)
                            #C.seekAC_XML.callproc('dbo.SPUpdateFlightsByRoutes', (ac, al + fn, db_air_route, flightdate, begindate))  # для pymssql (пока не ставится)
                            #Status = C.seekAC_XML.proc_status
                            #print(" Status = " + str(Status))
                            Data = C.seekAC_XML.fetchall()  # fetchval() - pyodbc convenience method similar to cursor.fetchone()[0]
                            C.cnxnAC_XML.commit()
                            if Data:
                                print(" Результат хранимой процедуры = " + str(Data))
                            Results.Result = 1
                        except pyodbc.Error as error:
                            sqlstate0 = error.args[0]
                            sqlstate1 = error.args[1]
                            print(" pyodbcErrors = " + str(sqlstate0.split(".")) + " , " + str(sqlstate1))
                            C.cnxnAC_XML.rollback()
                            Results.Result = 0
                        except Exception as exception:
                            print(" exception = " + str(exception))
                            C.cnxnAC_XML.rollback()
                            Results.Result = 0
                    else:
                        # fixme при полной модели восстановления БД на первых 5-ти загрузках файл журнала стал в 1000 раз больше файла данных -> сделал простую
                        try:
                            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
                            C.seekAC_XML.execute(SQLQuery)
                            XMLQuery = "SELECT FlightsByRoutes FROM dbo.AirCraftsTableNew2XsdIntermediate WITH (UPDLOCK) WHERE AirCraftRegistration = '" + str(ac) + "' "
                            C.seekAC_XML.execute(XMLQuery)
                            ResultXML = C.seekAC_XML.fetchone()
                            QuantityCounted = 1  # количество таких авиаперелетов за этот день
                            QuantityOnThisRoute = 1  # количестов авиаперелетов этого авиарейса по этому маршруту
                            QuantityOnThisFlight = 1  # количество авиаперелетов этого авиарейса
                            QuantityTotal = 1  # количество авиапрелетов с этой регистрацией
                            step = ElementTree.Element('step', FlightDate=str(flightdate), BeginDate=str(begindate))
                            Route = ElementTree.Element('Route', RouteFK=str(db_air_route))
                            Flight = ElementTree.Element('Flight', FlightNumberString=str(al) + str(fn))
                            root_tag_FlightsByRoutes = ElementTree.Element('FlightsByRoutes')
                            paddedStep = False
                            addedStep = False
                            addedRoute = False
                            addedFlight = False
                            if ResultXML[0] is None:
                                step.text = str(QuantityCounted)
                                Route.append(step)
                                #Flight.text = str(1)
                                Flight.append(Route)
                                #root_tag_FlightsByRoutes.text = str(1)
                                root_tag_FlightsByRoutes.append(Flight)
                                #Route.text = str(QuantityOnThisRoute)  # fixme в SSMS с этого места выводит в одну строчку (строка всегда в одну строчку)
                                addedStep = True
                                addedRoute = True
                                addedFlight = True
                            else:
                                root_tag_FlightsByRoutes = ElementTree.fromstring(ResultXML[0])
                                SearchFlight = root_tag_FlightsByRoutes.findall(".//Flight")
                                # fixme в БД наблюдаются дубликаты FlightNumberString, Route, step (цикл for ... break else ... работает не так, как ожидалось) -> добавил флаги added... , заменил else на if not added...
                                for nodeFlight in SearchFlight:
                                    if nodeFlight.attrib['FlightNumberString'] == str(al) + str(fn):
                                        SearchRoute = nodeFlight.findall(".//Route")
                                        for nodeRoute in SearchRoute:
                                            if nodeRoute.attrib['RouteFK'] == str(db_air_route):
                                                SearchStep = nodeRoute.findall(".//step")
                                                for nodeStep in SearchStep:
                                                    if nodeStep.attrib['FlightDate'] == str(flightdate) and not paddedStep:
                                                        QuantityCounted = int(nodeStep.text) + 1
                                                        nodeStep.text = str(QuantityCounted)
                                                        paddedStep = True
                                                        Results.Result = 2
                                                if not paddedStep:
                                                    step.text = str(QuantityCounted)
                                                    nodeRoute.append(step)
                                                    addedStep = True
                                                    Results.Result = 1
                                        if not paddedStep and not addedStep:
                                            step.text = str(QuantityCounted)
                                            Route.append(step)
                                            nodeFlight.append(Route)
                                            addedRoute = True
                                            Results.Result = 1
                                if not paddedStep and not addedStep and not addedRoute:
                                    step.text = str(QuantityCounted)
                                    Route.append(step)
                                    Flight.append(Route)
                                    root_tag_FlightsByRoutes.append(Flight)
                                    addedFlight = True
                                    Results.Result = 1
                            xml_FlightsByRoutes_to_String = ElementTree.tostring(root_tag_FlightsByRoutes, method='xml').decode(encoding="utf-8")  # XML-ная строка
                            XMLQuery = "UPDATE dbo.AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes = '" + str(xml_FlightsByRoutes_to_String) + "' WHERE AirCraftRegistration = '" + str(ac) + "' "
                            C.seekAC_XML.execute(XMLQuery)
                            C.cnxnAC_XML.commit()
                        except Exception:
                            C.cnxnAC_XML.rollback()
                            Results.Result = 0
                else:
                    try:
                        SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
                        C.seekFN.execute(SQLQuery)
                        SQLQuery = "SELECT * FROM dbo.AirFlightsTable WITH (UPDLOCK) WHERE FlightNumberString = '" + str(al) + str(fn) + "' AND AirRoute = "
                        SQLQuery += str(db_air_route) + " AND AirCraft = " + str(db_air_craft) + " AND FlightDate = '" + str(flightdate) + "' AND BeginDate = '" + str(begindate) + "' "
                        C.seekFN.execute(SQLQuery)
                        ResultQuery = C.seekFN.fetchone()
                        if ResultQuery is None:
                            SQLQuery = "INSERT INTO dbo.AirFlightsTable (AirRoute, AirCraft, FlightNumberString, QuantityCounted, FlightDate, BeginDate) VALUES ("
                            SQLQuery += str(db_air_route) + ", "  # bigint
                            SQLQuery += str(db_air_craft) + ", '"  # bigint
                            SQLQuery += str(al) + str(fn) + "', "  # nvarchar(50)
                            SQLQuery += str(1) + ", '" + str(flightdate) + "', '" + str(begindate) + "') "  # bigint
                            Results.Result = 1
                        elif ResultQuery is not None:
                            quantity = ResultQuery.QuantityCounted + 1
                            SQLQuery = "UPDATE dbo.AirFlightsTable SET QuantityCounted = " + str(quantity)
                            SQLQuery += " WHERE FlightNumberString = '" + str(al) + str(fn) + "' AND AirRoute = " + str(db_air_route)
                            SQLQuery += " AND AirCraft = " + str(db_air_craft) + " AND FlightDate = '" + str(flightdate) + "' AND BeginDate = '" + str(begindate) + "' "
                            Results.Result = 2
                        else:
                            pass
                        C.seekFN.execute(SQLQuery)
                        C.cnxnFN.commit()
                    except Exception:
                        C.cnxnFN.rollback()
                        Results.Result = 0
                    finally:
                        pass
            elif db_air_craft is None:
                Results.Result = 0
            else:
                Results.Result = 0
        elif db_air_route is None:
            Results.Result = 0
        else:
            Results.Result = 0
        return Results.Result

    def LoadThread(Csv, Log):
        """
        Читаем входной файл и перепаковываем его в DataFrame (кодировка UTF-8, шапка таблицы на столбцы, разделитель - ,)
        Источник BTSgov (убал из файла все косые, запятые и кавычки)
        https://www.transtats.bts.gov/DL_SelectFields.asp - не работает
        https://www.transtats.bts.gov/DL_SelectFields.asp?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr - работает
        """
        myDialog.label_execute.setText("Чтение и перепаковка исходных данных")
        myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: yellow")
        print("  Чтение и перепаковка исходных данных")
        print("  ожидайте ...", end=' ')
        # todo Если оперативной памяти не достаточно, то тут остановится
        DataFrameFromCSV = pandas.read_csv(Csv, sep=",")
        # В исходном файле *.csv подписаны столбцы -> в DataFrame можно перемещаться по именам столбцов -> Разбираем на столбцы и работаем с ними
        ListAirLineCodeIATA = DataFrameFromCSV['OP_UNIQUE_CARRIER'].tolist()
        ListAirCraft = DataFrameFromCSV['TAIL_NUM'].tolist()
        ListAirPortDeparture = DataFrameFromCSV['ORIGIN'].tolist()
        ListAirPortArrival = DataFrameFromCSV['DEST'].tolist()
        ListFlightNumber = DataFrameFromCSV['OP_CARRIER_FL_NUM'].tolist()
        # fixme Переделать эту часть (формат даты и времени в файле исходных данных поменялся с 2018-09-23 на 9/1/2023 12:00:00 AM)
        ListFlightDate = DataFrameFromCSV['FL_DATE'].tolist()
        # todo Собрать новый список с датами соединением из 3-х списков с целыми числами поэлементно через минусы и использовать теперь его -> СОБРАЛ
        # todo Проверить на соответствие результат перед записью в базу -> ПРОВЕРИЛ
        ListYear = DataFrameFromCSV['YEAR'].tolist()
        ListMonth = DataFrameFromCSV['MONTH'].tolist()
        ListDay = DataFrameFromCSV['DAY_OF_MONTH'].tolist()
        ListFlightDateConcatenated = []
        for attemptNumber in range(len(ListYear)):
            #ListFlightDateConcatenated.append(str(ListYear[attemptNumber]) + "-" + str(ListMonth[attemptNumber]) + "-" + str(ListDay[attemptNumber]))
            ListFlightDateConcatenated.append(str(ListYear[attemptNumber]) + "-" + '%02d' % ListMonth[attemptNumber] + "-" + '%02d' % ListDay[attemptNumber])
        #myDialog.label_execute.setText("Исходные данные перепакованы")  # оболочка зависает и слетает
        if Fl.SetInputDate:
            myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")
        else:
            myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: blue")
        print("Исходные данные перепакованы")
        # Списки
        ListAirLinesAdded = []
        ListAirLinesFailed = []
        ListAirCraftsAdded = []
        ListAirCraftsUpdated = []
        ListAirCraftsFailed = []
        ListAirPortsNotFounded = []
        # Счетчики
        CountRoutesAdded = 0
        CountRoutesFailed = 0
        CountFlightsAdded = 0
        CountFlightsPadded = 0
        CountFlightsFailed = 0
        CountProgressBarFailed = 0
        # Распределение плотности перезапросов сервера
        DistributionDensityAirLines = []
        DistributionDensityAirCrafts = []
        DistributionDensityAirRoutes = []
        DistributionDensityAirFlights = []
        Density = 2  # раз в секунду
        # attemptRetryCount = 750 * Density
        attemptRetryCount = 750  # увеличить, если появятся несплюсованные и невставленные авиаперелеты
        for Index in range(attemptRetryCount):
            DistributionDensityAirLines.append(0)
            DistributionDensityAirCrafts.append(0)
            DistributionDensityAirRoutes.append(0)
            DistributionDensityAirFlights.append(0)
        # Дата и время сейчас
        Now = time.time()
        DateTime = time.ctime(Now)
        # Отметка времени начала загрузки
        StartTime = datetime.datetime.now()
        #myDialog.label_execute.setText("Загрузка начата")  # оболочка зависает и слетает
        print(termcolor.colored("Загрузка начата", "red", "on_yellow"))
        # Сигнал на обновление полоски выполнения
        completion = 0  # Выполнение загрузки
        ExecutePrevious = 0
        # Один внешний цикл и три вложенных цикла
        for AL, AC, Dep, Arr, FN, FD in zip(ListAirLineCodeIATA, ListAirCraft, ListAirPortDeparture, ListAirPortArrival, ListFlightNumber, ListFlightDateConcatenated):
            print(colorama.Fore.BLUE + "Авикомпания", str(AL), end=" ")
            deadlockCount = 0  # Счетчик попыток -> Обнуляем
            # Цикл попыток
            for attemptNumber in range(attemptRetryCount):
                deadlockCount = attemptNumber
                DBAirLine = A.QueryAirLineByIATA(AL)
                if DBAirLine is None:
                    if A.InsertAirLineByIATAandICAO(AL, None):
                        ListAirLinesAdded.append(AL)
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # оболочка зависает и слетает
                        print(colorama.Fore.GREEN + "вставилась ", end=" ")
                        break
                    else:
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                        print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                        time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                elif DBAirLine is not None:
                    break
                else:
                    #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                    print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                    time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
            else:
                ListAirLinesFailed.append(AL)
            print(" ")
            DistributionDensityAirLines[deadlockCount] += 1
            print(colorama.Fore.BLUE + " Самолет", str(AC), end=" ")
            deadlockCount = 0  # Счетчик попыток -> Обнуляем
            # Цикл попыток
            for attemptNumber in range(attemptRetryCount):
                deadlockCount = attemptNumber
                DBAirCraft = C.QueryAirCraftByRegistration(AC, Fl.useAirCraftsDSN)
                if DBAirCraft is None:
                    DBAirLine = A.QueryAirLineByIATA(AL)
                    if DBAirLine is None:
                        # Вставляем самолет с пустым внешним ключем
                        if C.InsertAirCraftByRegistration(Registration=AC, ALPK=None, useAirCrafts=Fl.useAirCraftsDSN):
                            ListAirCraftsAdded.append(AC)
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # оболочка зависает и слетает
                            print(colorama.Fore.GREEN + "вставился", end=" ")
                            break
                        else:
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                            print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                            time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                    elif DBAirLine is not None:
                        # Вставляем самолет (на предыдущем цикле вставили авиакомпанию)
                        if C.InsertAirCraftByRegistration(Registration=AC, ALPK=DBAirLine.AirLineUniqueNumber, useAirCrafts=Fl.useAirCraftsDSN):
                            ListAirCraftsAdded.append(AC)
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # оболочка зависает и слетает
                            print(colorama.Fore.GREEN + "вставился", end=" ")
                            break
                        else:
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                            print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                            time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                    else:
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                        print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                        time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                elif DBAirCraft is not None:
                    if Fl.useAirCraftsDSN:
                        break
                    else:
                        DBAirLinePK = A.QueryAirLineByPK(DBAirCraft.AirCraftAirLine)
                        if DBAirLinePK is None or DBAirLinePK.AirLineCodeIATA != AL:
                            # fixme пустая ячейка в таблице SQL-ной БД - NULL <-> в Python-е - (None,) -> в условиях None и (None,) - не False и не True
                            # fixme Просмотрел таблицу самолетов скриптом на SQL -> регистрация UNKNOWN не имеет внешнего ключа авиакомпании
                            # fixme Просмотрел таблицу самолетов скриптом на SQL -> регистрация nan каждый раз переписывается на другую компанию-оператора
                            DBAirLine = A.QueryAirLineByIATA(AL)
                            if DBAirLine is None:
                                break
                            elif DBAirLine is not None:
                                if C.UpdateAirCraft(Registration=AC, ALPK=DBAirLine.AirLineUniqueNumber, useAirCrafts=Fl.useAirCraftsDSN):
                                    ListAirCraftsUpdated.append(AC)
                                    #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # оболочка зависает и слетает
                                    print(colorama.Fore.LIGHTCYAN_EX + "переписали на", str(AL), end=" ")
                                    break
                                else:
                                    #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                                    print(colorama.Fore.LIGHTYELLOW_EX + "*", end=" ")
                                    time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                            else:
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                                print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                                time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                        elif DBAirLinePK.AirLineCodeIATA == AL:
                            break
                        else:
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                            print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                            time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                else:
                    #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                    print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                    time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
            else:
                ListAirCraftsFailed.append(AC)
            print(" ")
            DistributionDensityAirCrafts[deadlockCount] += 1
            print(colorama.Fore.BLUE + " Маршрут", str(Dep), "-", str(Arr), end=" ")
            deadlockCount = 0  # Счетчик попыток -> Обнуляем
            # Цикл попыток
            for attemptNumber in range(attemptRetryCount):
                deadlockCount = attemptNumber
                DBAirPortDep = P.QueryAirPortByIATA(Dep)
                if DBAirPortDep is not None:
                    DBAirPortArr = P.QueryAirPortByIATA(Arr)
                    if DBAirPortArr is not None:
                        DBAirRoute = P.QueryAirRoute(Dep, Arr)
                        if DBAirRoute is None:
                            # Если есть оба аэропорта и нет маршрута
                            if P.InsertAirRoute(DBAirPortDep.AirPortUniqueNumber, DBAirPortArr.AirPortUniqueNumber):
                                CountRoutesAdded += 1
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # оболочка зависает и слетает
                                print(colorama.Fore.GREEN + "вставился", end=" ")
                                break
                            else:
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                                print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                                time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                        elif DBAirRoute is not None:
                            break
                        else:
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                            print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                            time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                    elif DBAirPortArr is None:
                        ListAirPortsNotFounded.append(Arr)
                        # Вставляем аэропорт только с кодом IATA
                        if P.InsertAirPortByIATA(Arr):
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # оболочка зависает и слетает
                            print(colorama.Fore.GREEN + "вставили аэропорт", str(Arr), end=" ")
                        else:
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                            print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                            time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                    else:
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                        print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                        time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                elif DBAirPortDep is None:
                    ListAirPortsNotFounded.append(Dep)
                    # Вставляем аэропорт только с кодом IATA
                    if P.InsertAirPortByIATA(Dep):
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # оболочка зависает и слетает
                        print(colorama.Fore.GREEN + "вставили аэропорт", str(Dep), end=" ")
                    else:
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                        print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                        time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                else:
                    #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                    print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                    time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
            else:
                CountRoutesFailed += 1
            print(" ")
            DistributionDensityAirRoutes[deadlockCount] += 1
            print(colorama.Fore.BLUE + " Авиарейс", str(AL) + str(FN), end=" ")
            deadlockCount = 0  # Счетчик попыток -> Обнуляем
            if not Fl.SetInputDate:
                FD = Fl.BeginDate
            # Цикл попыток
            for attemptNumber in range(attemptRetryCount):
                deadlockCount = attemptNumber
                DBAirLine = A.QueryAirLineByIATA(AL)
                if DBAirLine is not None:
                    DBAirCraft = C.QueryAirCraftByRegistration(AC, Fl.useAirCraftsDSN)
                    if DBAirCraft is not None:
                        DBAirRoute = P.QueryAirRoute(Dep, Arr)
                        if DBAirRoute is not None:
                            # todo между транзакциями маршрут и самолет еще раз перезапросить внутри вызываемой функции - СДЕЛАЛ
                            #ResultModify = ModifyFlight.ModifyAirFlight(C, P, AC, AL, FN, Dep, Arr, FD, Fl.BeginDate, Fl.useAirCraftsDSN, Fl.useXQuery)
                            ResultModify = ModifyAirFlight(AC, AL, FN, Dep, Arr, FD, Fl.BeginDate, Fl.useAirCraftsDSN, Fl.useXQuery)
                            if ResultModify == 0:
                                # fixme оболочка зависает и слетает
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                                print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                                time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                            if ResultModify == 1:
                                CountFlightsAdded += 1
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # оболочка зависает и слетает
                                print(colorama.Fore.GREEN + "вставился", end=" ")
                                break
                            if ResultModify == 2:
                                CountFlightsPadded += 1
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # оболочка зависает и слетает
                                print(colorama.Fore.GREEN + "сплюсовался", end=" ")
                                break
                        elif DBAirRoute is None:
                            CountFlightsFailed += 1
                            break
                        else:
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                            print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                            time.sleep(attemptNumber / Density)
                    elif DBAirCraft is None:
                        CountFlightsFailed += 1
                        break
                    else:
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                        print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                        time.sleep(attemptNumber / Density)
                elif DBAirLine is None:
                    CountFlightsFailed += 1
                    break
                else:
                    #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                    print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                    time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
            else:
                CountFlightsFailed += 1
            print(" ")
            DistributionDensityAirFlights[deadlockCount] += 1
            completion += 1
            Execute = round(100 * completion / len(ListFlightNumber), 2)  # вычисляем и округляем процент выполнения до 2 цифр после запятой
            # fixme При слишком частом обновлении виджета графическая оболочка подвисает, зависает или слетает (обработка исключения не помогает) -> Исправил
            if Execute > ExecutePrevious:
                stringExecute = "Выполнение = " + str(Execute) + " %"
                myDialog.label_execute.setText(stringExecute)
                ExecutePrevious = Execute
            # todo Сделать полосу выполнения все время внизу со всеми параметрами например с помощью tqdm - Не работает в цикле
            print(colorama.Fore.CYAN + "Выполнение =", str(Execute), "%")
        # Отметка времени окончания загрузки
        EndTime = datetime.datetime.now()
        # Убираем с конца столбцы с нулями
        for Index in reversed(range(attemptRetryCount)):
            if DistributionDensityAirLines[Index] == 0 and DistributionDensityAirCrafts[Index] == 0 and DistributionDensityAirRoutes[Index] == 0 and DistributionDensityAirFlights[Index] == 0:
                DistributionDensityAirLines.pop(Index)
                DistributionDensityAirCrafts.pop(Index)
                DistributionDensityAirRoutes.pop(Index)
                DistributionDensityAirFlights.pop(Index)
            else:
                break
        # Собираем списки в DataFrame
        DataFrameDistributionDensity = pandas.DataFrame([DistributionDensityAirLines,
                                                         DistributionDensityAirCrafts,
                                                         DistributionDensityAirRoutes,
                                                         DistributionDensityAirFlights],
                                                        index=[" - авиакомпании", " - самолеты", " - маршруты", " - авиарейсы"])
        DataFrameDistributionDensity.index.name = "Базы данных:"
        OutputString = " \n \n"
        OutputString += "Загрузка рабочих данных (версия обработки - " + str(myOwnDevelopingVersion) + ") начата " + str(DateTime) + " \n"
        OutputString += " Загрузка проведена с " + str(socket.gethostname()) + " \n"
        OutputString += " Версия интерпретатора = " + str(sys.version) + " \n"
        #OutputString += " Источник входных данных = " + str(F.InputFileCSV) + " \n"
        OutputString += " Входные данные внесены за " + str(Fl.BeginDate) + " \n"
        if Fl.SetInputDate:
            OutputString += " Дата авиарейса проставлена из входного файла\n"
        else:
            OutputString += " Дата авиарейса проставлена как 1-ое число указанного месяца \n"
        DataSQL = C.getSQLData()
        if Fl.useAirCraftsDSN:
            OutputString += " Авиаперелеты загружены в БД самолетов "
            if Fl.useXQuery:
                OutputString += " с помощью xQuery (SAX) \n"
            else:
                OutputString += " с помощью xml.etree.ElementTree (DOM) \n"
        OutputString += " Сервер СУБД = " + str(DataSQL[0]) + " \n"
        OutputString += " Драйвер = " + str(DataSQL[1]) + " \n"
        OutputString += " Версия ODBC = " + str(DataSQL[2]) + " \n"
        OutputString += " DSN = " + str(DataSQL[3]) + " \n"
        OutputString += " Схема = " + str(DataSQL[4]) + " \n"
        OutputString += " Длительность загрузки = " + str(EndTime - StartTime) + " \n"
        OutputString += " Пользователь = " + str(os.getlogin()) + " \n"
        OutputString += " Итоги: \n"
        # Формируем итоги
        # todo Сделать итоги в виде XML и писать его полем XML.Document в базу данных
        if ListAirLinesAdded:
            OutputString += " - вставились авиакомпании: \n  "
            OutputString += str(set(ListAirLinesAdded))  # fixme с регистрациями NaN надолго зависает, не убирает повторы и не группирует -> данные без регистрации не загужаем
            OutputString += " \n"
        if ListAirLinesFailed:
            OutputString += " - не вставились данные по авиакомпаниям: \n  "
            OutputString += str(set(ListAirLinesFailed))
            OutputString += " \n"
        if ListAirCraftsAdded:
            OutputString += " - вставили самолеты: \n  "
            OutputString += str(set(ListAirCraftsAdded))
            OutputString += " \n"
        if ListAirCraftsUpdated:
            OutputString += " - добавлены данные по самолетам: \n  "
            OutputString += str(set(ListAirCraftsUpdated))
            # Убираем только повторы, идущие подряд, но с сохранением исходного порядка fixme не работает
            OutPutNew = [el for el, _ in itertools.groupby(ListAirCraftsUpdated)]
            OutputString += " \n"
        if ListAirCraftsFailed:
            OutputString += " - не добавлены данные по самолетам: \n  "
            OutputString += str(set(ListAirCraftsFailed))
            OutputString += " \n"
        if CountRoutesAdded:
            OutputString += " - вставились " + str(CountRoutesAdded) + " маршруты \n"
        if CountRoutesFailed:
            OutputString += " - не вставились " + str(CountRoutesFailed) + " маршруты \n"
            OutputString += " \n"
        if ListAirPortsNotFounded:
            OutputString += " - не найдены аэропорты: \n  "
            OutputString += str(set(ListAirPortsNotFounded))
            OutputString += " \n"
        if CountFlightsAdded:
            OutputString += " - вставились " + str(CountFlightsAdded) + " авиарейсы \n"
        if CountFlightsFailed:
            OutputString += " - не вставились " + str(CountFlightsFailed) + " авиарейсы \n"
        if CountFlightsPadded:
            OutputString += " - сплюсовались " + str(CountFlightsPadded) + " авиарейсы \n"
        OutputString += " - перезапросы сервера: \n" + str(DataFrameDistributionDensity) + " \n"
        # Дописываем в журнал (обычным способом)
        # fixme Большая строка не дописывается, скрипт долго висит -> Исправил
        try:
            # fixme При больших объемах дозаписи и одновременном доступе к журналу нескольких обработок не все результаты дописываются в него -> Исправил
            LogFile = open(Log, 'a')
            LogFile.write(OutputString)
            # LogFile.write('Вывод обычным способом\n')
        except IOError:
            try:
                LogError = open(F.ErrorFileTXT, 'a')
                LogError.write("Ошибка дозаписи результатов по " + str(F.InputFileCSV) + " в " + str(F.InputFileCSV) + " \n")
            except IOError:
                print("Ошибка дозаписи в файл журнала")
            finally:
                LogError.close()
            print(colorama.Fore.LIGHTYELLOW_EX + "Ошибка дозаписи в " + str(FileNames.LogFileTXT))
        finally:
            LogFile.close()
        # Дописываем в журнал (с помощью менеджера контекста)
        # with open(Log, 'a') as LogFile:
        #     LogFile.write(OutputString)
        #     LogFile.write('Вывод с помощью менеджера контекста\n')
        myDialog.label_execute.setText("Загрузка окончена")
        myDialog.label_22.setStyleSheet("border: 5px solid; border-color: pink")  # fixme Тут графическая оболочка слетела -> Задержка не дала результат -> Исправил
        print(termcolor.colored("Загрузка окончена", "red", "on_yellow"))
        A.disconnectAL()
        P.disconnectRT()
        if Fl.useAirCraftsDSN:
            C.disconnectAC_XML()
        else:
            C.disconnectAC()
            C.disconnectFN()

    def PushButtonGetStarted():
        myDialog.pushButton_GetStarted.setEnabled(False)
        Fl.BeginDate = myDialog.dateEdit_BeginDate.date().toString('yyyy-MM-dd')
        if myDialog.checkBox_SetInputDate.isChecked():
            Fl.SetInputDate = True
        else:
            Fl.SetInputDate = False
        myDialog.pushButton_ChooseCSVFile.setEnabled(False)
        myDialog.pushButton_ChooseTXTFile.setEnabled(False)
        myDialog.dateEdit_BeginDate.setEnabled(False)
        myDialog.checkBox_SetInputDate.setEnabled(False)
        myDialog.pushButton_Disconnect_AL.setEnabled(False)
        myDialog.pushButton_Disconnect_RT.setEnabled(False)
        myDialog.pushButton_Disconnect_AC.setEnabled(False)
        myDialog.label_execute.setEnabled(True)
        # todo Заброс на возможность запуска нескольких загрузок с доработкой графической оболочки без ее закрытия на запуске загрузки
        threadLoad = threading.Thread(target=LoadThread, daemon=False, args=(F.InputFileCSV, F.LogFileTXT, ))  # поток не сам по себе
        threadLoad.start()
        # fixme с ... .join() кнопки не гаснут, графическая оболочка зависает -> убрал ... .join()
        #threadLoad.join(1)  # ждем поток в основном потоке (графическая оболочка зависает), секунд
        #myDialog.close()  # закрываем графическую оболочку, текстовая остается

    # Отрисовка диалога
    myDialog.show()
    # Правильное закрытие диалога
    sys.exit(myApp.exec_())


# Точка входа
# __name__ — это специальная переменная, которая будет равна __main__,
# только если файл запускается как основная программа, в остальных случаях - имени модуля при импорте в качестве модуля
if __name__ == "__main__":
    myApplication()
