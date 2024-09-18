#  Interpreter 3.7 -> 3.10


import pandas
import itertools
import datetime
import time
import os
import sys
import socket
import threading
from configparser import ConfigParser
import logging

from PyQt5 import QtWidgets  # оставил 5-ую версию (много наработок еще завязаны на нее)
import pathlib
import colorama
import termcolor

# Импорт модуля библиотек индивидуальной разработки
from modulesFilesWithClasses.moduleClasses import FileNames, Flags, States, ACFN
from modulesFilesWithClasses.moduleClassesUIsSources import Ui_DialogLoadAirFlightsWithAirCrafts
# todo  - Сделать пользовательскую наработку (не библиотеку и не пакет) отдельным репозиторием
#       - Импортировать ее как подмодуль для повторного применения синхронно (mutualy connected) или асинхронно (independent) -> Импортировал асинхронно, обновление только вручную на командах git, для синхронного нет функционала
#       - Результат импорта -> на github-е - синяя неактивная ссылка, по которой никуда не перейдешь, внутри pyCharm-а - дубликат репозитория подмодуля в локальную ветку
# fixme pyCharm как графическая оболочка пока не работает с подмодулями в графическом режиме [@Aleks10](https://qna.habr.com/q/196071), а пока только командами 'git submodules'


# Добавляем функционал
# Делаем свои рабочие экземпляры
config_from_cfg = ConfigParser()
config_from_cfg.read('configCommon.cfg')

acfn = ACFN()

F = FileNames()
F.filenameCSV = ' '
F.filenameTXT = ' '
F.filenameLOG = ' '

Fl = Flags()
Fl.current_user = os.getlogin()
Fl.current_hostname = socket.gethostname()
Fl.current_interpreter_version = sys.version
Fl.useSQLServerDriverFormat = True

St = States()

logger = logging.getLogger(__name__)

myOwnDevelopingVersion = config_from_cfg.getfloat(section='ConstantParameters', option='myOwnDevelopingVersion')  # Версия

colorama.init(autoreset=False)  # используем Colorama и Termcolor на Windows, оставляем цветовое оформление до следующего явного указания
print(termcolor.colored("Загрузка рабочих данных v" + str(myOwnDevelopingVersion) + " в БД SQL Server-а", 'blue', 'on_yellow'))
print("Разработал Тарасов Сергей tsv19su@yandex.ru")
print(termcolor.colored("Пользователь = " + str(Fl.current_user), 'green', 'on_yellow'))

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
    DSNs = sorted(acfn.getDataSources())  # добавленные системные DSN-ы
    if DSNs:
        for DSN in DSNs:
            if 'AirCraft' in DSN:
                myDialog.comboBox_DSN_AC.addItem(str(DSN))
            if 'AirFlight' in DSN:
                myDialog.comboBox_DSN_FN.addItem(str(DSN))
    # Получаем список драйверов баз данных
    # Добавляем атрибут DriversODBC по ходу действия
    DriversODBC = sorted(acfn.getSQLDrivers())
    if DriversODBC:
        for DriverODBC in DriversODBC:
            myDialog.comboBox_Driver_AL.addItem(str(DriverODBC))
            myDialog.comboBox_Driver_RT.addItem(str(DriverODBC))
            myDialog.comboBox_Driver_FN.addItem(str(DriverODBC))
    # Добавляем базы данных в выпадающие списки
    listdbs = sorted(config_from_cfg.get(section='DataBases', option='AirLines').split(','))
    if listdbs:
        for point in listdbs:
            #point = point.lstrip(' ')
            stripped_point = point.strip()  # todo см. статью https://stackoverflow.com/questions/959215/how-do-i-remove-leading-whitespace-in-python
            myDialog.comboBox_DB_AL.addItem(stripped_point)
    listdbs = sorted(config_from_cfg.get(section='DataBases', option='AirPorts').split(','))
    if listdbs:
        for point in listdbs:
            #point = point.lstrip(' ')
            stripped_point = point.strip()
            myDialog.comboBox_DB_RT.addItem(stripped_point)
    listdbs = sorted(config_from_cfg.get(section='DataBases', option='FlightsAndCrafts').split(','))
    if listdbs:
        for point in listdbs:
            #point = point.lstrip(' ')
            stripped_point = point.strip()
            myDialog.comboBox_DB_FN.addItem(stripped_point)
    myDialog.dateEdit_BeginDate.setToolTip("Дата начала периода загрузки рабочих данных")
    myDialog.checkBox_SetInputDate.setToolTip("Перенос даты авиарейса из входных данных")
    myDialog.pushButton_GetStarted.setToolTip("Запуск загрузки исходных данных по авиаперелетам \nВнимательно проверьте параметры загрузки")
    myDialog.radioButton_DSN_AirCrafts_DOM.setToolTip("Ресурсозатратный, медленный на больших объемах данных\nПри использовании ПОЛНОЙ модели восстановления БД\n данный метод мягко говоря сильно загружает файл журнала *.ldf")
    myDialog.radioButton_DSN_AirCrafts_SAX.setToolTip("Быстрый. Использует функционал XML-ного поля + XML-ный индекс\nМожно выставить в свойствах БД модель восстановления - ПОЛНАЯ")
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
            if St.Connected_RT and (St.Connected_ACFN or St.Connected_AC):
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
            if St.Connected_AL and (St.Connected_ACFN or St.Connected_AC):
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
        if St.Connected_AC or St.Connected_ACFN:
            # Переключаем в рабочее состояние
            myDialog.comboBox_DB_FN.setEnabled(False)  # mssql
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
            if Fl.useAirCrafts:
                myDialog.groupBox_2.setEnabled(True)
                if Fl.useAirCraftsDB:
                    if Fl.useXQuery:
                        myDialog.checkBox_SetUseMSSQL.setEnabled(True)
                        if Fl.useMSsql:
                            myDialog.checkBox_SetUseODBCMarkers.setEnabled(False)
                        else:
                            myDialog.checkBox_SetUseODBCMarkers.setEnabled(True)
                    else:
                        myDialog.checkBox_SetUseMSSQL.setEnabled(False)
                        myDialog.checkBox_SetUseODBCMarkers.setEnabled(False)
                    myDialog.comboBox_DB_FN.setEnabled(True)
                    myDialog.comboBox_Driver_FN.setEnabled(True)
                    myDialog.comboBox_DSN_FN.setEnabled(False)
                    myDialog.comboBox_DSN_AC.setEnabled(False)
                else:
                    if Fl.useXQuery:
                        if Fl.useMSsql:
                            myDialog.checkBox_SetUseODBCMarkers.setEnabled(False)
                        else:
                            myDialog.checkBox_SetUseODBCMarkers.setEnabled(True)
                        myDialog.checkBox_SetUseMSSQL.setEnabled(True)
                    else:
                        myDialog.checkBox_SetUseMSSQL.setEnabled(False)
                        myDialog.checkBox_SetUseODBCMarkers.setEnabled(False)
                    myDialog.comboBox_DB_FN.setEnabled(False)
                    myDialog.comboBox_Driver_FN.setEnabled(False)
                    myDialog.comboBox_DSN_FN.setEnabled(False)
                    myDialog.comboBox_DSN_AC.setEnabled(True)
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
            PrepareForInputData(False)

    def RadioButtonsDataSourcesToggled():
        # Переключатели -> Флаги
        if myDialog.radioButton_DB_AirCrafts.isChecked() or myDialog.radioButton_DSN_AirCrafts.isChecked():
            Fl.useAirCrafts = True
            if myDialog.radioButton_DB_AirCrafts.isChecked():
                Fl.useAirCraftsDB = True
            if myDialog.radioButton_DSN_AirCrafts.isChecked():
                Fl.useAirCraftsDB = False
        else:
            Fl.useAirCrafts = False
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
        UpdateFlightsSourcesChoiceByStatesAndFlags()

    def CheckBoxUseMssql():
        if myDialog.checkBox_SetUseMSSQL.isChecked():
            Fl.useMSsql = True
        else:
            Fl.useMSsql = False
        UpdateFlightsSourcesChoiceByStatesAndFlags()

    def CheckBoxUseOdbcMarkers():
        if myDialog.checkBox_SetUseODBCMarkers.isChecked():
            Fl.useODBCMarkers = True
        else:
            Fl.useODBCMarkers = False

    UpdateAirLinesSourcesChoiceByStatesAndFlags()
    UpdateAirPortsSourcesChoiceByStatesAndFlags()
    RadioButtonsDataSourcesToggled()
    RadioButtonsXQueryToggled()
    UpdateFlightsSourcesChoiceByStatesAndFlags()
    myDialog.pushButton_Disconnect_AL.setEnabled(False)
    myDialog.pushButton_Disconnect_RT.setEnabled(False)
    myDialog.pushButton_Disconnect_AC.setEnabled(False)
    myDialog.pushButton_GetStarted.setEnabled(False)
    myDialog.label_execute.setEnabled(False)

    # Привязки обработчиков todo без lambda не работает
    myDialog.radioButton_DB_AirFlights.toggled.connect(lambda: RadioButtonsDataSourcesToggled())
    myDialog.radioButton_DSN_AirFlights.toggled.connect(lambda: RadioButtonsDataSourcesToggled())
    myDialog.radioButton_DSN_AirCrafts.toggled.connect(lambda: RadioButtonsDataSourcesToggled())
    myDialog.radioButton_DSN_AirCrafts_DOM.toggled.connect(lambda: RadioButtonsXQueryToggled())
    myDialog.radioButton_DSN_AirCrafts_SAX.toggled.connect(lambda: RadioButtonsXQueryToggled())
    myDialog.checkBox_SetUseMSSQL.stateChanged.connect(lambda: CheckBoxUseMssql())
    myDialog.checkBox_SetUseODBCMarkers.stateChanged.connect(lambda: CheckBoxUseOdbcMarkers())
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
            # todo https://docs.microsoft.com/ru-ru/previous-versions/dotnet/framework/data/adonet/sql/ownership-and-user-schema-separation-in-sql-server
            ChoiceDB = myDialog.comboBox_DB_AL.currentText()
            ChoiceDriver = myDialog.comboBox_Driver_AL.currentText()
            # Добавляем атрибуты DataBase, DriverODBC
            DataBase_AL = str(ChoiceDB)
            DriverODBC_AL = str(ChoiceDriver)
            if acfn.connectDB_AL_odbc(servername=config_from_cfg.get(section='Servers', option='ServerNameRemote'), driver=DriverODBC_AL, database=DataBase_AL):
                print("  БД = ", DataBase_AL, "подключена")
                Data = acfn.getSQLData_odbc()
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
            acfn.disconnectAL_odbc()
            St.Connected_AL = False
        # Переключаем в исходное состояние
        UpdateAirLinesSourcesChoiceByStatesAndFlags()
        myDialog.pushButton_Connect_AL.setEnabled(True)

    def PushButtonConnect_ACFN():
        if Fl.useAirCrafts:
            myDialog.pushButton_Connect_AC.setEnabled(False)
            if not St.Connected_AC:
                # Подключаемся к базе данных самолетов
                # todo Схема по умолчанию - dbo, другая схема указывается в явном виде
                ChoiceDB_AC_mssql = myDialog.comboBox_DB_FN.currentText()
                ChoiceDriver_AC_mssql = myDialog.comboBox_Driver_FN.currentText()
                DataBase_ACFN = str(ChoiceDB_AC_mssql)
                DriverODBC_ACFN = str(ChoiceDriver_AC_mssql)
                ChoiceDSN_AC_odbc = myDialog.comboBox_DSN_AC.currentText()
                myDSN_AC_odbc = str(ChoiceDSN_AC_odbc)
                # fixme не подключается по pymssql
                if Fl.useAirCraftsDB:
                    if Fl.useXQuery and Fl.useMSsql:
                        if acfn.connectDB_AC_odbc(servername=config_from_cfg.get(section='Servers', option='ServerNameRemote'), driver=DriverODBC_ACFN, database=DataBase_ACFN) and acfn.connectDB_AC_mssql(servername=config_from_cfg.get(section='Servers', option='ServerNameRemote'), database=DataBase_ACFN):
                            St.Connected_AC = True
                    else:
                        if acfn.connectDB_AC_odbc(servername=config_from_cfg.get(section='Servers', option='ServerNameRemote'), driver=DriverODBC_ACFN, database=DataBase_ACFN):
                            St.Connected_AC = True
                else:
                    if Fl.useXQuery and Fl.useMSsql:
                        if acfn.connectDSN_AC_odbc(dsn=myDSN_AC_odbc) and acfn.connectDB_AC_mssql(servername=config_from_cfg.get(section='Servers', option='ServerNameRemote'), database=DataBase_ACFN):
                            St.Connected_AC = True
                    else:
                        if acfn.connectDSN_AC_odbc(dsn=myDSN_AC_odbc):
                            St.Connected_AC = True
                if St.Connected_AC:
                    if Fl.useXQuery and Fl.useMSsql:
                        Data = acfn.getSQLData_mssql()
                    else:
                        Data = acfn.getSQLData_odbc()
                    print(" Data = " + str(Data))
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
                DataBase_ACFN = str(ChoiceDB_ACFN)
                DriverODBC_ACFN = str(ChoiceDriver_ACFN)
                ChoiceDSN_ACFN = myDialog.comboBox_DSN_FN.currentText()
                myDSN_ACFN = str(ChoiceDSN_ACFN)
                if Fl.useAirFlightsDB:
                    if acfn.connectDB_ACFN_odbc(servername=config_from_cfg.get(section='Servers', option='ServerNameRemote'), driver=DriverODBC_ACFN, database=DataBase_ACFN):
                        St.Connected_ACFN = True
                else:
                    if acfn.connectDSN_ACFN_odbc(myDSN_ACFN):
                        St.Connected_ACFN = True
                if St.Connected_ACFN:
                    Data = acfn.getSQLData_odbc()
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
        if St.Connected_AC:
            acfn.disconnectAC_odbc()
            if Fl.useXQuery and Fl.useMSsql:
                acfn.disconnectAC_mssql()
            acfn.disconnectACFN_odbc()
            St.Connected_AC = False
        if St.Connected_ACFN:
            acfn.disconnectACFN_odbc()
            St.Connected_ACFN = False
        UpdateFlightsSourcesChoiceByStatesAndFlags()
        myDialog.pushButton_Connect_AC.setEnabled(True)

    def PushButtonConnect_RT():
        myDialog.pushButton_Connect_RT.setEnabled(False)
        if not St.Connected_RT:
            # Подключаемся к базе данных аэропортов и маршрутов
            # todo Схема по умолчанию - dbo, другая схема указывается в явном виде
            ChoiceDB = myDialog.comboBox_DB_RT.currentText()
            ChoiceDriver = myDialog.comboBox_Driver_RT.currentText()
            # Добавляем атрибуты DataBase, DriverODBC
            DataBase_RT = str(ChoiceDB)
            DriverODBC_RT = str(ChoiceDriver)
            if acfn.connectDB_RT_odbc(servername=config_from_cfg.get(section='Servers', option='ServerNameRemote'), driver=DriverODBC_RT, database=DataBase_RT):
                print("  БД = ", DataBase_RT, "подключена")
                Data = acfn.getSQLData_odbc()
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
            acfn.disconnectRT_odbc()
            St.Connected_RT = False
        # Переключаем в исходное состояние
        UpdateAirPortsSourcesChoiceByStatesAndFlags()
        myDialog.pushButton_Connect_RT.setEnabled(True)

    def LoadThread(Csv, Log):
        """
        Читаем входной файл и перепаковываем его в DataFrame (кодировка UTF-8, шапка таблицы на столбцы, разделитель - ,)
        Источник BTSgov (todo убрать из файла все косые, запятые и кавычки)
        https://www.transtats.bts.gov/DL_SelectFields.asp - не работает
        https://www.transtats.bts.gov/DL_SelectFields.asp?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr - работает
        """
        myDialog.label_execute.setText("Чтение и перепаковка исходных данных")
        myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: yellow")
        print("  Чтение и перепаковка исходных данных")
        print("  ожидайте ...", end=' ')
        logger.info("Чтение и перепаковка исходных данных")
        # todo Если оперативной памяти не достаточно, то тут остановится
        DataFrameFromCSV = pandas.read_csv(Csv, sep=",")
        if Fl.SetInputDate:
            myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")
        else:
            myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: blue")
        print("Исходные данные перепакованы")
        logger.info("Исходные данные перепакованы")
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
        CountFlightsInserted = 0
        CountFlightsFailed = 0
        CountProgressBarFailed = 0
        # Распределение плотности перезапросов сервера
        DistributionDensityAirLines = []
        DistributionDensityAirCrafts = []
        DistributionDensityAirRoutes = []
        DistributionDensityAirFlights = []
        Density = config_from_cfg.getint(section='ConstantParameters', option='Density')  # раз в секунду
        # attemptRetryCount = 750 * Density
        attemptRetryCount = config_from_cfg.getint(section='ConstantParameters', option='attemptRetryCount')
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
        logger.info("Загрузка начата")
        # Сигнал на обновление полоски выполнения
        completion = 0  # Выполнение загрузки
        Execute = 0
        ExecutePrevious = 0
        # Один внешний цикл и три вложенных цикла
        # todo Высота DataFrame см. https://stackoverflow.com/questions/15943769/how-do-i-get-the-row-count-of-a-pandas-dataframe
        for slider in range(len(DataFrameFromCSV.index)):
            # todo Получение элемента по номеру строки и имени столбца см. https://stackoverflow.com/questions/70931002/pandas-get-cell-value-by-row-index-and-column-name
            AL = DataFrameFromCSV.iloc[slider, DataFrameFromCSV.columns.get_loc('OP_UNIQUE_CARRIER')]
            AC = DataFrameFromCSV.iloc[slider, DataFrameFromCSV.columns.get_loc('TAIL_NUM')]
            Dep = DataFrameFromCSV.iloc[slider, DataFrameFromCSV.columns.get_loc('ORIGIN')]
            Arr = DataFrameFromCSV.iloc[slider, DataFrameFromCSV.columns.get_loc('DEST')]
            FN = DataFrameFromCSV.iloc[slider, DataFrameFromCSV.columns.get_loc('OP_CARRIER_FL_NUM')]
            Year_from_DataFrameFromCSV = DataFrameFromCSV.iloc[slider, DataFrameFromCSV.columns.get_loc('YEAR')]
            Month_from_DataFrameFromCSV = DataFrameFromCSV.iloc[slider, DataFrameFromCSV.columns.get_loc('MONTH')]
            Day_from_DataFrameFromCSV = DataFrameFromCSV.iloc[slider, DataFrameFromCSV.columns.get_loc('DAY_OF_MONTH')]
            FD = str(Year_from_DataFrameFromCSV) + "-" + '%02d' % Month_from_DataFrameFromCSV + "-" + '%02d' % Day_from_DataFrameFromCSV
            print(colorama.Fore.BLUE + "Авиакомпания", str(AL), end=" ")
            deadlockCount = 0  # Счетчик попыток -> Обнуляем
            # Цикл попыток
            for attemptNumber in range(attemptRetryCount):
                deadlockCount = attemptNumber
                DBAirLine = acfn.QueryAirLineByIATA(AL)
                if DBAirLine is None:
                    if acfn.InsertAirLineByIATAandICAO(AL, None):
                        ListAirLinesAdded.append(AL)
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # оболочка зависает и слетает
                        print(colorama.Fore.GREEN + "вставилась ", end=" ")
                        break
                    else:
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                        print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                        logger.debug(" - ожидание вставки авиакомпании " + str(AL))
                        time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                elif DBAirLine is not None:
                    break
                else:
                    #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                    print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                    logger.debug(" - перезапрос авиакомпании " + str(AL))
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
                DBAirCraft = acfn.QueryAirCraftByRegistration(AC, Fl.useAirCrafts)
                if DBAirCraft is None:
                    DBAirLine = acfn.QueryAirLineByIATA(AL)
                    if DBAirLine is None:
                        # Вставляем самолет с пустым внешним ключем
                        if acfn.InsertAirCraftByRegistration(Registration=AC, ALPK=None, useAirCrafts=Fl.useAirCrafts):
                            ListAirCraftsAdded.append(AC)
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # fixme оболочка зависает и слетает
                            print(colorama.Fore.GREEN + "вставился", end=" ")
                            break
                        else:
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # fixme оболочка зависает и слетает
                            print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                            logger.debug(" - ожидание вставки самолета " + str(AC) + " неизвестной авиакомпании")
                            time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                    elif DBAirLine is not None:
                        # Вставляем самолет (на предыдущем проходе вставили авиакомпанию)
                        if acfn.InsertAirCraftByRegistration(Registration=AC, ALPK=DBAirLine.AirLineUniqueNumber, useAirCrafts=Fl.useAirCrafts):
                            ListAirCraftsAdded.append(AC)
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # fixme оболочка зависает и слетает
                            print(colorama.Fore.GREEN + "вставился", end=" ")
                            break
                        else:
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # fixme оболочка зависает и слетает
                            print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                            logger.debug(" - ожидание вставки самолета " + str(AC) + " авиакомпании " + str(AL))
                            time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                    else:
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # fixme оболочка зависает и слетает
                        print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                        logger.debug(" - перезапрос авиакомпании " + str(AL))
                        time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                elif DBAirCraft is not None:
                    if Fl.useAirCrafts:
                        break
                    else:
                        DBAirLinePK = acfn.QueryAirLineByPK(DBAirCraft.AirCraftAirLine)
                        if DBAirLinePK is None or DBAirLinePK.AirLineCodeIATA != AL:
                            # fixme пустая ячейка в таблице SQL-ной БД - NULL <-> в Python-е - (None,) -> в условиях None и (None,) - не False и не True
                            # fixme Просмотрел таблицу самолетов скриптом на SQL -> регистрация UNKNOWN не имеет внешнего ключа авиакомпании
                            # fixme Просмотрел таблицу самолетов скриптом на SQL -> регистрация nan каждый раз переписывается на другую компанию-оператора
                            DBAirLine = acfn.QueryAirLineByIATA(AL)
                            if DBAirLine is None:
                                break
                            elif DBAirLine is not None:
                                if acfn.UpdateAirCraft(Registration=AC, ALPK=DBAirLine.AirLineUniqueNumber, useAirCrafts=Fl.useAirCrafts):
                                    ListAirCraftsUpdated.append(AC)
                                    #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # fixme оболочка зависает и слетает
                                    print(colorama.Fore.LIGHTCYAN_EX + "переписали на", str(AL), end=" ")
                                    break
                                else:
                                    #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # fixme оболочка зависает и слетает
                                    print(colorama.Fore.LIGHTYELLOW_EX + "*", end=" ")
                                    logger.debug(" - ожидание изменения авиакомпании " + str(AL) + " самолета " + str(AC))
                                    time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                            else:
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # fixme оболочка зависает и слетает
                                print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                                logger.debug(" - перезапрос авиакомпании " + str(AL))
                                time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                        elif DBAirLinePK.AirLineCodeIATA == AL:
                            break
                        else:
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # fixme оболочка зависает и слетает
                            print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                            logger.debug(" - перезапрос авиакомпании " + str(AL))
                            time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                else:
                    #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # fixme оболочка зависает и слетает
                    print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                    logger.debug(" - перезапрос самолета " + str(AC))
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
                DBAirPortDep = acfn.QueryAirPortByIATA(Dep)
                if DBAirPortDep is not None:
                    DBAirPortArr = acfn.QueryAirPortByIATA(Arr)
                    if DBAirPortArr is not None:
                        DBAirRoute = acfn.QueryAirRoute(Dep, Arr)
                        if DBAirRoute is None:
                            # Если есть оба аэропорта и нет маршрута
                            if acfn.InsertAirRoute(DBAirPortDep.AirPortUniqueNumber, DBAirPortArr.AirPortUniqueNumber):
                                CountRoutesAdded += 1
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # fixme оболочка зависает и слетает
                                print(colorama.Fore.GREEN + "вставился", end=" ")
                                break
                            else:
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # fixme оболочка зависает и слетает
                                print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                                logger.debug(" - ожидание вставки маршрута " + str(Dep) + "-" + str(Arr))
                                time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                        elif DBAirRoute is not None:
                            break
                        else:
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # fixme оболочка зависает и слетает
                            print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                            logger.debug(" - перезапрос маршрута " + str(Dep) + "-" + str(Arr))
                            time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                    elif DBAirPortArr is None:
                        ListAirPortsNotFounded.append(Arr)
                        # Вставляем аэропорт только с кодом IATA
                        if acfn.InsertAirPortByIATA(Arr):
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # fixme оболочка зависает и слетает
                            print(colorama.Fore.GREEN + "вставили аэропорт", str(Arr), end=" ")
                        else:
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # fixme оболочка зависает и слетает
                            print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                            logger.debug(" - ожидание вставки аэропорта " + str(Arr))
                            time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                    else:
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # fixme оболочка зависает и слетает
                        print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                        logger.debug(" - перезапрос аэропорта " + str(Arr))
                        time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                elif DBAirPortDep is None:
                    ListAirPortsNotFounded.append(Dep)
                    # Вставляем аэропорт только с кодом IATA
                    if acfn.InsertAirPortByIATA(Dep):
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # fixme оболочка зависает и слетает
                        print(colorama.Fore.GREEN + "вставили аэропорт", str(Dep), end=" ")
                    else:
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # fixme оболочка зависает и слетает
                        print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                        logger.debug(" - ожидание вставки аэропорта " + str(Dep))
                        time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                else:
                    #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # fixme оболочка зависает и слетает
                    print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                    logger.debug(" - перезапрос аэропорта " + str(Dep))
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
                DBAirLine = acfn.QueryAirLineByIATA(AL)
                if DBAirLine is not None:
                    DBAirCraft = acfn.QueryAirCraftByRegistration(AC, Fl.useAirCrafts)
                    if DBAirCraft is not None:
                        DBAirRoute = acfn.QueryAirRoute(Dep, Arr)
                        if DBAirRoute is not None:
                            # todo между транзакциями маршрут и самолет еще раз перезапросить внутри вызываемой функции - СДЕЛАЛ
                            ResultModify = acfn.ModifyAirFlight(AC, AL, FN, Dep, Arr, FD, Fl.BeginDate, Fl.useAirCrafts, Fl.useXQuery, Fl.useMSsql, Fl.useODBCMarkers, Fl.useSQLServerDriverFormat)
                            if ResultModify == 0:
                                # fixme оболочка зависает и слетает
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # fixme оболочка зависает и слетает
                                print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                                logger.debug(" - несработка вставки (изменения) " + str(AC) + "авиарейса \t " + str(AL) + str(FN) + "\t " + str(Dep) + "-" + str(Arr) + "\t " + str(FD))
                                time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                            if ResultModify == 1:
                                CountFlightsAdded += 1
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # fixme оболочка зависает и слетает
                                print(colorama.Fore.GREEN + "вставился", end=" ")
                                break
                            if ResultModify == 2:
                                CountFlightsPadded += 1
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # fixme оболочка зависает и слетает
                                print(colorama.Fore.GREEN + "сплюсовался", end=" ")
                                break
                            if ResultModify == 3:
                                CountFlightsInserted += 1
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # fixme оболочка зависает и слетает
                                print(colorama.Fore.GREEN + "записался с нуля новый", end=" ")
                                break
                        elif DBAirRoute is None:
                            CountFlightsFailed += 1
                            break
                        else:
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # fixme оболочка зависает и слетает
                            print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                            logger.debug(" - перезапрос маршрута " + str(AC) + "\t" + str(AL) + str(FN) + "\t" + str(Dep) + "-" + str(Arr) + "\t" + str(FD))
                            time.sleep(attemptNumber / Density)
                    elif DBAirCraft is None:
                        CountFlightsFailed += 1
                        break
                    else:
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # fixme оболочка зависает и слетает
                        print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                        logger.debug(" - перезапрос самолета " + str(AC) + "\t " + str(AL) + str(FN) + "\t " + str(Dep) + "-" + str(Arr) + "\t " + str(FD))
                        time.sleep(attemptNumber / Density)
                elif DBAirLine is None:
                    CountFlightsFailed += 1
                    break
                else:
                    #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # fixme оболочка зависает и слетает
                    print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                    logger.debug(" - перезапрос авиакомпании " + str(AC) + "\t " + str(AL) + str(FN) + "\t " + str(Dep) + "-" + str(Arr) + "\t " + str(FD))
                    time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
            else:
                CountFlightsFailed += 1
            print(" ")
            DistributionDensityAirFlights[deadlockCount] += 1
            completion += 1
            Execute = round(100 * completion / len(DataFrameFromCSV.index), 2)  # вычисляем и округляем процент выполнения до 2 цифр после запятой
            # fixme При слишком частом обновлении виджета графическая оболочка подвисает, зависает или слетает (обработка исключения не помогает) -> Исправил
            if Execute > ExecutePrevious:
                stringExecute = "Выполнение = " + str(Execute) + " %"
                myDialog.label_execute.setText(stringExecute)
                ExecutePrevious = Execute
            print(colorama.Fore.CYAN + "Выполнение =", str(Execute), "%")
            """
            if not acfn.checkConnection():
                St.Connected_AL = False
                St.Connected_AC = False
                St.Connected_ACFN = False
                St.Connected_RT = False
                break
            """
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
        if St.Connected_AL and (St.Connected_AC or St.Connected_ACFN) and St.Connected_RT:
            myDialog.label_execute.setText("Загрузка окончена")
            myDialog.label_22.setStyleSheet("border: 5px solid; border-color: pink")  # fixme Тут графическая оболочка слетела -> Задержка не дала результат -> Исправил
            print(termcolor.colored("Загрузка окончена", "red", "on_yellow"))
            #F.filenameTXT = pathlib.Path(F.OutputFileTXT).name
            logger.info("Загрузка окончена. Результаты см. в " + F.filenameTXT + " в папке Журналов")
            OutputString = " \n \n"
            OutputString += "Загрузка рабочих данных (версия обработки - " + str(myOwnDevelopingVersion) + ") начата " + str(DateTime) + " \n"
            OutputString += " Загрузка проведена с " + str(Fl.current_hostname) + " \n"
            OutputString += " Версия интерпретатора = " + str(Fl.current_interpreter_version) + " \n"
            #F.filenameCSV = pathlib.Path(F.InputFileCSV).name
            OutputString += " Источник входных данных = " + F.filenameCSV + " \n"
            OutputString += " Входные данные внесены через DataFrameFromCSV за " + str(Fl.BeginDate) + " \n"
            if Fl.SetInputDate:
                OutputString += " Дата авиарейса проставлена из входного файла\n"
            else:
                OutputString += " Дата авиарейса проставлена как 1-ое число указанного месяца \n"
            DataSQL = acfn.getSQLData_odbc()
            if Fl.useAirCrafts:
                OutputString += " Авиаперелеты загружены в БД самолетов с помощью "
                if Fl.useXQuery:
                    OutputString += "SQL-ных хранимок со вставками на xPath & xQuery (как SAX)"
                    if Fl.useMSsql:
                        OutputString += " и mssql \n"
                        DataSQL = acfn.getSQLData_mssql()
                    elif Fl.useODBCMarkers:
                        OutputString += " с маркерами pyODBC \n"
                    else:
                        OutputString += " \n"
                else:
                    OutputString += "xml.etree.ElementTree (как DOM) \n"
            else:
                OutputString += " Авиаперелеты загружены в БД авиаперелетов \n"
            OutputString += " Сервер СУБД = " + str(DataSQL[0]) + " \n"
            OutputString += " Драйвер = " + str(DataSQL[1]) + " \n"
            OutputString += " Версия ODBC = " + str(DataSQL[2]) + " \n"
            OutputString += " DSN = " + str(DataSQL[3]) + " \n"
            OutputString += " Схема (пользователь) = " + str(DataSQL[4]) + " \n"
            OutputString += " Длительность загрузки = " + str(EndTime - StartTime) + " \n"
            OutputString += " Пользователь = " + str(Fl.current_user) + " \n"
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
            if CountFlightsInserted:
                OutputString += " - записались с нуля " + str(CountFlightsInserted) + " авиарейсы \n"
            if CountFlightsFailed:
                OutputString += " - не вставились " + str(CountFlightsFailed) + " авиарейсы \n"
            if CountFlightsPadded:
                OutputString += " - сплюсовались " + str(CountFlightsPadded) + " авиарейсы \n"
            OutputString += " - перезапросы сервера: \n" + str(DataFrameDistributionDensity) + " \n"
            # Дописываем в журнал (обычным способом)
            # fixme Большая строка не дописывается, скрипт долго висит -> Исправил
            LogFile = None
            LogErrorFile = None
            try:
                # fixme При больших объемах дозаписи и одновременном доступе к журналу нескольких обработок не все результаты дописываются в него -> Исправил
                LogFile = open(Log, 'a')
                LogFile.write(OutputString)
                # LogFile.write('Вывод обычным способом\n')
            except IOError:
                try:
                    LogErrorFile = open(F.OutputFileTXTErrors, 'a')
                    LogErrorFile.write("Ошибка дозаписи результатов по " + str(F.filenameCSV) + " в " + str(F.filenameTXT) + " \n")
                except IOError:
                    print("Ошибка дозаписи в файл журнала")
                finally:
                    LogErrorFile.close()
                print(colorama.Fore.LIGHTYELLOW_EX + "Ошибка дозаписи в " + str(F.filenameTXT))
                logger.error("Ошибка дозаписи в " + str(F.filenameTXT))
            finally:
                LogFile.close()
            #logging.info(OutputString)
            # Дописываем в журнал (с помощью менеджера контекста)
            # with open(Log, 'a') as LogFile:
            #     LogFile.write(OutputString)
            #     LogFile.write('Вывод с помощью менеджера контекста\n')
        else:
            stringExecute = "Соединение с СУБД прервано на " + str(Execute) + " %"
            myDialog.label_execute.setText(stringExecute)
            myDialog.label_22.setStyleSheet("border: 5px solid; border-color: red")
            print(termcolor.colored("Соединение с СУБД прервано на " + str(Execute) + " % ", "red", "on_yellow"))
            logger.error("Соединение с СУБД прервано на " + str(Execute) + " % ")
        acfn.disconnectAL_odbc()
        if Fl.useAirCrafts:
            acfn.disconnectAC_odbc()
            if Fl.useMSsql:
                acfn.disconnectAC_mssql()
        else:
            acfn.disconnectACFN_odbc()
        acfn.disconnectRT_odbc()

    def PushButtonChooseCSVFile():
        filter = config_from_cfg.get(section='Paths', option='filterCSV')
        #filter = "Data files (*.csv)"
        F.InputFileCSV = QtWidgets.QFileDialog.getOpenFileName(None, "Открыть рабочие данные", ' ', filter=filter)[0]
        urnCSV = F.InputFileCSV.rstrip(os.sep)  # fixme не сработало
        F.filenameCSV = pathlib.Path(F.InputFileCSV).name
        myDialog.lineEdit_CSVFile.setText(F.filenameCSV)

    def PushButtonChooseTXTFile():
        filter = config_from_cfg.get(section='Paths', option='filterLOG')
        #filter = "Log Files (*.txt *.text)"
        F.OutputFileTXT = QtWidgets.QFileDialog.getOpenFileName(None, "Открыть журнал", ' ', filter=filter)[0]
        F.filenameTXT = pathlib.Path(F.OutputFileTXT).name
        myDialog.lineEdit_TXTFile.setText(F.filenameTXT)

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
        F.filenameCSV = pathlib.Path(F.InputFileCSV).name
        #LogFileNamePreffix = filenameCSV.rsplit('.', 1)[0]
        LogFileNamePreffix = F.filenameCSV
        LogFileNameSuffix = config_from_cfg.get(section='Paths', option='LogFileNameSuffix')
        F.filenameLOG = "P:\\Programming\\Python Scripts\\LoadWorkData - GUIs and Utilities\\Протоколы загрузки\\" + LogFileNamePreffix.removesuffix('.csv') + LogFileNameSuffix
        print(" LogFileName = " + str(F.filenameLOG))
        logging.basicConfig(filename=F.filenameLOG, filemode="w", format="%(asctime)s %(levelname)s %(message)s")
        # todo При отладке из-под учетки разработчика - уровень DEBUG, при нормальной работе - INFO
        if config_from_cfg.getboolean(section='ConstantParameters', option='DebugLevel') and (Fl.current_user == config_from_cfg.get(section='UserLogins', option='Developer')):
            #logging.basicConfig(level=logging.DEBUG, filename=F.filenameLOG, filemode="w", format="%(asctime)s %(levelname)s %(message)s")
            logger.setLevel(level=logging.DEBUG)
        else:
            #logging.basicConfig(level=logging.INFO, filename=F.filenameLOG, filemode="w", format="%(asctime)s %(levelname)s %(message)s")
            logger.setLevel(level=logging.INFO)
        logger.info("Загрузка рабочих данных v" + str(myOwnDevelopingVersion) + " в БД SQL Server-а")
        logger.debug(" в режиме отладки")
        #logger.warning("a WARNING")
        #logger.error("an ERROR")
        #logger.critical("a message of CRITICAL severity")
        # todo Заброс на возможность запуска нескольких загрузок с доработкой графической оболочки без ее закрытия на запуске загрузки
        threadLoad = threading.Thread(target=LoadThread, daemon=False, args=(F.InputFileCSV, F.OutputFileTXT,))  # поток не сам по себе
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
