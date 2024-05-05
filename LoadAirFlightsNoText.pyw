#  Interpreter 3.7 -> 3.10


import pyodbc  # pymssql работает тяжелее, пробуем также SQLAlchemy
import pandas
import itertools
import datetime
import time
import os
import sys
import socket
import threading
from xml.etree import ElementTree
# оставили 5-ую версию, потому что много наработок еще завязаны на нее
# QtCore, QtGui, QtNetwork, QtOpenGL, QtScript, QtSQL (медленнее чем pyodbc), QtDesigner - запускаем в командной строке, QtXml (устарел) -> замена QXmlStreamReader, QXmlStreamWriter
from PyQt5 import QtWidgets
import pathlib
#import stringcolor  # fixme в IDLE и в pyCharm раскраска не работает, в командной строке сразу слетает
import colorama
import termcolor
#import tqdm  # fixme tqdm нужен свой цикл -> сюда не подходит

# Импорт пользовательской библиотеки (файла *.py в этой же папке)
import Classes
# todo  - Сделать пользовательскую наработку (не библиотеку и не пакет) отдельным репозиторием
#       - Импортировать ее как подмодуль для повторного применения синхронно (mutualy connected) или асинхронно (independent) -> Импортировал асинхронно, обновление только вручную на командах git, для синхронного нет функционала
#       - Результат импорта -> на github-е - синяя неактивная ссылка, по которой никуда не перейдешь, внутри pyCharm-а - дубликат репозитория подмодуля в локальную ветку
# fixme Есть проблемка при импорте пользовательских библиотек из внешних файлов по другим путям из других папок
# fixme pyCharm как графическая оболочка пока не работает с подмодулями в графическом режиме [@Aleks10](https://qna.habr.com/q/196071), а пока только командами 'git submodules'


# Версия обработки с цветным выводом
myOwnDevelopingVersion = 8.7
# todo Версия задается тут. Пакеты на GitHub-е *.tar.gz (под Linux или под BSD) не нужны. Выпуск релизов пока не имеет практической пользы, как указано в ReadME.md

colorama.init(autoreset=False)  # используем Colorama, чтобы сделать работу Termcolor на Windows, оставляем цветовое оформление до следующего явного указания
print(termcolor.colored("Обработка v" + str(myOwnDevelopingVersion) + " загрузки рабочих данных в БД SQL Server-а", 'blue', 'on_yellow'))
print("Разработал Тарасов Сергей tsv19su@yandex.ru")
#print("Разработал " + stringcolor.bold("Тарасов Сергей").cs("red", "gold") + " tsv19su@yandex.ru")
print(termcolor.colored("Пользователь = " + str(os.getlogin()), 'green', 'on_yellow'))

# fixme Вывести в файл requirements.txt список пакетов с версиями - пока не требуется
# pip freeze > requirements.txt

# fixme Установить пакеты с определенными версиями - пока не требуется
# pip install -r requirements.txt

# fixme Установить пакет из папки, как пример
# pip install SomePackage-1.0-py2.py3-none-any.whl

# Делаем экземпляр
S = Classes.Servers()


# Имена серверов
class ServerNames:
    #ServerNameOriginal = "data-server-1.movistar.vrn.skylink.local"
    ServerNameOriginal = "localhost\mssqlserver15"  # указал имя NetBIOS и указал инстанс
    #ServerNameOriginal = "localhost\sqldeveloper"  # указал инстанс
    # fixme Забыл отменить обратно, надо проверить как самолеты и авиарейсы грузились без него причем в рабочую базу -> Все нормально, этот выбор работал, если грузить не через системный DSN
    ServerNameFlights = "data-server-1.movistar.vrn.skylink.local"  # указал ресурсную запись из DNS
    ServerName = "localhost\mssqlserver15"  # указал инстанс
    #ServerName = "localhost\sqldeveloper"  # указал инстанс
    cnxnAL = ' '
    cnxnRT = ' '
    cnxnAC_XML = ' '
    cnxnAC = ' '
    cnxnFN = ' '
    seekAL = ' '
    seekRT = ' '
    seekAC_XML = ' '
    seekAC = ' '
    seekFN = ' '


# Имена читаемых и записываемых файлов
class FileNames:
    InputFileCSV = ' '
    LogFileTXT = ' '
    ErrorFileTXT = 'LogReport_Errors.txt'


# Флаги
class Flags:
    useAirFlightsDB = True
    useAirCraftsDSN = False
    useXQuery = False
    SetInputDate = False
    BeginDate = ' '


# Состояния
class States:
    Connected_AL = False
    Connected_RT = False
    Connected_ACFN = False
    Connected_AC_XML = False


def myApplication():
    # Одно прикладное приложение
    myApp = QtWidgets.QApplication(sys.argv)
    # Делаем экземпляры
    myDialog = Classes.Ui_DialogLoadAirFlightsWithAirCrafts()
    myDialog.setupUi(Dialog=myDialog)  # надо вызывать явно
    myDialog.setFixedSize(940, 375)
    myDialog.setWindowTitle('Загрузка рабочих данных')
    # Дополняем функционал экземпляра главного диалога
    # Переводим в исходное состояние
    myDialog.label_Version.setText("Версия обработки " + str(myOwnDevelopingVersion))
    # Получаем список DSN-ов
    # Добавляем атрибут DSNs по ходу действия
    ServerNames.DSNs = pyodbc.dataSources()  # добавленные системные DSN-ы
    if ServerNames.DSNs:
        for DSN in ServerNames.DSNs:
            if not DSN:
                break
            myDialog.comboBox_DSN_FN.addItem(str(DSN))
            myDialog.comboBox_DSN_AC.addItem(str(DSN))
    # Получаем список драйверов баз данных
    # Добавляем атрибут DriversODBC по ходу действия
    ServerNames.DriversODBC = pyodbc.drivers()
    if ServerNames.DriversODBC:
        for DriverODBC in ServerNames.DriversODBC:
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
        #myDialog.checkBox_SetInputDate.setChecked(False)
        if Key:
            myDialog.dateEdit_BeginDate.setCalendarPopup(True)
        myDialog.checkBox_SetInputDate.setEnabled(Key)
        myDialog.pushButton_GetStarted.setEnabled(Key)

    def UpdateAirLinesSourcesChoiceByStatesAndFlags():
        if States.Connected_AL:
            # Переключаем в рабочее состояние
            myDialog.comboBox_DB_AL.setEnabled(False)
            myDialog.comboBox_Driver_AL.setEnabled(False)
            if States.Connected_RT and (States.Connected_ACFN or States.Connected_AC_XML):
                PrepareForInputData(True)
        else:
            # Переключаем в исходное состояние
            if not States.Connected_RT:
                myDialog.lineEdit_Server.setEnabled(False)
            myDialog.lineEdit_Driver_AL.setEnabled(False)
            myDialog.lineEdit_ODBCversion_AL.setEnabled(False)
            myDialog.lineEdit_Schema_AL.setEnabled(False)
            myDialog.comboBox_DB_AL.setEnabled(True)
            myDialog.comboBox_Driver_AL.setEnabled(True)
            PrepareForInputData(False)

    def UpdateAirPortsSourcesChoiceByStatesAndFlags():
        if States.Connected_RT:
            # Переключаем в рабочее состояние
            myDialog.comboBox_DB_RT.setEnabled(False)
            myDialog.comboBox_Driver_RT.setEnabled(False)
            if States.Connected_AL and (States.Connected_ACFN or States.Connected_AC_XML):
                PrepareForInputData(True)
        else:
            # Переключаем в исходное состояние
            if not States.Connected_AL:
                myDialog.lineEdit_Server.setEnabled(False)
            myDialog.lineEdit_Driver_RT.setEnabled(False)
            myDialog.lineEdit_ODBCversion_RT.setEnabled(False)
            myDialog.lineEdit_Schema_RT.setEnabled(False)
            myDialog.comboBox_DB_RT.setEnabled(True)
            myDialog.comboBox_Driver_RT.setEnabled(True)
            PrepareForInputData(False)

    def UpdateFlightsSourcesChoiceByStatesAndFlags():
        # Состояния + Флаги -> Графическая оболочка
        if States.Connected_AC_XML or States.Connected_ACFN:
            # Переключаем в рабочее состояние
            myDialog.comboBox_DB_FN.setEnabled(False)
            myDialog.comboBox_Driver_FN.setEnabled(False)
            myDialog.comboBox_DSN_FN.setEnabled(False)
            myDialog.comboBox_DSN_AC.setEnabled(False)
            myDialog.groupBox.setEnabled(False)
            myDialog.groupBox_2.setEnabled(False)
            if States.Connected_AL and States.Connected_RT:
                PrepareForInputData(True)
        else:
            # Переключаем в исходное состояние
            myDialog.lineEdit_Server_remote.setEnabled(False)
            myDialog.lineEdit_Driver_AC.setEnabled(False)
            myDialog.lineEdit_ODBCversion_AC.setEnabled(False)
            myDialog.lineEdit_Schema_AC.setEnabled(False)
            myDialog.lineEdit_DSN_AC.setEnabled(False)
            myDialog.groupBox.setEnabled(True)
            if Flags.useAirCraftsDSN:
                myDialog.comboBox_DB_FN.setEnabled(False)
                myDialog.comboBox_Driver_FN.setEnabled(False)
                myDialog.comboBox_DSN_FN.setEnabled(False)
                myDialog.comboBox_DSN_AC.setEnabled(True)
                myDialog.groupBox_2.setEnabled(True)
            else:
                myDialog.comboBox_DSN_AC.setEnabled(False)
                myDialog.groupBox_2.setEnabled(False)
                if Flags.useAirFlightsDB:
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
            Flags.useAirCraftsDSN = True
        else:
            Flags.useAirCraftsDSN = False
            if myDialog.radioButton_DB_AirFlights.isChecked():
                Flags.useAirFlightsDB = True
            if myDialog.radioButton_DSN_AirFlights.isChecked():
                Flags.useAirFlightsDB = False
        UpdateFlightsSourcesChoiceByStatesAndFlags()

    def RadioButtonsXQueryToggled():
        if myDialog.radioButton_DSN_AirCrafts_DOM.isChecked():
            Flags.useXQuery = False
        if myDialog.radioButton_DSN_AirCrafts_SAX.isChecked():
            Flags.useXQuery = True

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
    # todo Объединить radioButton, как на tkBuilder, и переделать на triggered
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
        if not States.Connected_AL:
            # Подключаемся к базе данных авиакомпаний
            # todo Схема по умолчанию - dbo, другая схема указывается в явном виде
            # https://docs.microsoft.com/ru-ru/previous-versions/dotnet/framework/data/adonet/sql/ownership-and-user-schema-separation-in-sql-server
            ChoiceDB = myDialog.comboBox_DB_AL.currentText()
            ChoiceDriver = myDialog.comboBox_Driver_AL.currentText()
            # Добавляем атрибуты DataBase, DriverODBC
            ServerNames.DataBase_AL = str(ChoiceDB)
            ServerNames.DriverODBC_AL = str(ChoiceDriver)
            try:
                # Добавляем атрибут cnxn
                # через драйвер СУБД + клиентский API-курсор
                # todo Сделать сообщение с зелеными галочками по пунктам подключения
                ServerNames.cnxnAL = pyodbc.connect(driver=ServerNames.DriverODBC_AL, server=ServerNames.ServerNameOriginal, database=ServerNames.DataBase_AL)
                print("  БД = ", ServerNames.DataBase_AL, "подключена")
                # Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде, в СУБД по умолчанию FALSE
                ServerNames.cnxnAL.autocommit = False
                print("autocommit is disabled")
                # Делаем свой экземпляр и ставим набор курсоров
                # КУРСОР нужен для перехода функционального языка формул на процедурный или для вставки процедурных кусков в функциональный скрипт.
                #
                # Способы реализации курсоров:
                #  - SQL, Transact-SQL,
                #  - серверные API-курсоры (OLE DB, ADO, ODBC),
                #  - клиентские API-курсоры (выборка кэшируется на клиенте)
                #
                # API-курсоры ODBC по SQLSetStmtAttr:
                #  - тип SQL_ATTR_CURSOR_TYPE:
                #    - однопроходный (последовательный доступ),
                #    - статический (копия в tempdb),
                #    - управляемый набор ключей,
                #    - динамический,
                #    - смешанный
                #  - режим работы в стиле ISO:
                #    - прокручиваемый SQL_ATTR_CURSOR_SCROLLABLE,
                #    - обновляемый (чувствительный) SQL_ATTR_CURSOR_SENSITIVITY

                # Клиентские однопроходные , статические API-курсоры ODBC.
                # Добавляем атрибуты seek...
                ServerNames.seekAL = ServerNames.cnxnAL.cursor()
                print("seeks is on")
                States.Connected_AL = True
                # Переключаем в рабочее состояние
                # SQL Server
                myDialog.lineEdit_Server.setEnabled(True)
                myDialog.lineEdit_Server.setText(ServerNames.cnxnAL.getinfo(pyodbc.SQL_SERVER_NAME))
                # Драйвер
                myDialog.lineEdit_Driver_AL.setEnabled(True)
                myDialog.lineEdit_Driver_AL.setText(ServerNames.cnxnAL.getinfo(pyodbc.SQL_DRIVER_NAME))
                # версия ODBC
                myDialog.lineEdit_ODBCversion_AL.setEnabled(True)
                myDialog.lineEdit_ODBCversion_AL.setText(ServerNames.cnxnAL.getinfo(pyodbc.SQL_ODBC_VER))
                # Схема (если из-под другой учетки, то выводит имя учетки)
                myDialog.lineEdit_Schema_AL.setEnabled(True)
                myDialog.lineEdit_Schema_AL.setText(ServerNames.cnxnAL.getinfo(pyodbc.SQL_USER_NAME))
                # Переводим в рабочее состояние (продолжение)
                UpdateAirLinesSourcesChoiceByStatesAndFlags()
                myDialog.pushButton_Disconnect_AL.setEnabled(True)
            except Exception:
                myDialog.pushButton_Connect_AL.setEnabled(True)
                message = QtWidgets.QMessageBox()
                message.setText("Нет подключения к базе данных авиакомпаний")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
            else:
                pass
            finally:
                pass

    def PushButtonDisconnect_AL():
        # Обработчик кнопки 'Отключиться от базы данных'
        myDialog.pushButton_Disconnect_AL.setEnabled(False)
        if States.Connected_AL:
            # Снимаем курсор
            ServerNames.seekAL.close()
            # Отключаемся от базы данных
            ServerNames.cnxnAL.close()
            States.Connected_AL = False
        # Переключаем в исходное состояние
        UpdateAirLinesSourcesChoiceByStatesAndFlags()
        myDialog.pushButton_Connect_AL.setEnabled(True)

    def PushButtonConnect_RT():
        myDialog.pushButton_Connect_RT.setEnabled(False)
        if not States.Connected_RT:
            # Подключаемся к базе данных аэропортов и маршрутов
            # todo Схема по умолчанию - dbo, другая схема указывается в явном виде
            ChoiceDB = myDialog.comboBox_DB_RT.currentText()
            ChoiceDriver = myDialog.comboBox_Driver_RT.currentText()
            # Добавляем атрибуты DataBase, DriverODBC
            ServerNames.DataBase_RT = str(ChoiceDB)
            ServerNames.DriverODBC_RT = str(ChoiceDriver)
            try:
                # Добавляем атрибут cnxn
                # через драйвер СУБД + клиентский API-курсор
                ServerNames.cnxnRT = pyodbc.connect(driver=ServerNames.DriverODBC_RT, server=ServerNames.ServerNameOriginal, database=ServerNames.DataBase_RT)
                print("  БД = ", ServerNames.DataBase_RT, "подключена")
                # Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде, в СУБД по умолчанию FALSE
                ServerNames.cnxnRT.autocommit = False
                print("autocommit is disabled")
                # Делаем свой экземпляр и ставим набор курсоров
                # КУРСОР нужен для перехода функционального языка формул на процедурный или для вставки процедурных кусков в функциональный скрипт.
                #
                # Способы реализации курсоров:
                #  - SQL, Transact-SQL,
                #  - серверные API-шные курсоры (OLE DB, ADO, ODBC),
                #  - клиентские API-шные курсоры (выборка кэшируется на клиенте)
                #
                # API-шные курсоры ODBC по SQLSetStmtAttr:
                #  - тип SQL_ATTR_CURSOR_TYPE:
                #    - однопроходный (последовательный доступ),
                #    - статический (копия в tempdb),
                #    - управляемый набор ключей,
                #    - динамический,
                #    - смешанный
                #  - режим работы в стиле ISO:
                #    - прокручиваемый SQL_ATTR_CURSOR_SCROLLABLE,
                #    - обновляемый (чувствительный) SQL_ATTR_CURSOR_SENSITIVITY

                # Клиентские однопроходные, статические API-курсоры ODBC.
                # Добавляем атрибуты seek...
                ServerNames.seekRT = ServerNames.cnxnRT.cursor()
                print("seeks is on")
                States.Connected_RT = True
                # Переключаем в рабочее состояние
                # SQL Server
                myDialog.lineEdit_Server.setText(ServerNames.cnxnRT.getinfo(pyodbc.SQL_SERVER_NAME))
                myDialog.lineEdit_Server.setEnabled(True)
                # Драйвер
                myDialog.lineEdit_Driver_RT.setText(ServerNames.cnxnRT.getinfo(pyodbc.SQL_DRIVER_NAME))
                myDialog.lineEdit_Driver_RT.setEnabled(True)
                # версия ODBC
                myDialog.lineEdit_ODBCversion_RT.setText(ServerNames.cnxnRT.getinfo(pyodbc.SQL_ODBC_VER))
                myDialog.lineEdit_ODBCversion_RT.setEnabled(True)
                # Схема (если из-под другой учетки, то выводит имя учетки)
                myDialog.lineEdit_Schema_RT.setText(ServerNames.cnxnRT.getinfo(pyodbc.SQL_USER_NAME))
                myDialog.lineEdit_Schema_RT.setEnabled(True)
                # Переводим в рабочее состояние (продолжение)
                UpdateAirPortsSourcesChoiceByStatesAndFlags()
                myDialog.pushButton_Disconnect_RT.setEnabled(True)
            except Exception:
                myDialog.pushButton_Connect_RT.setEnabled(True)
                message = QtWidgets.QMessageBox()
                message.setText("Нет подключения к базе данных аэропортов и маршрутов")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
            else:
                pass
            finally:
                pass

    def PushButtonDisconnect_RT():
        # Обработчик кнопки 'Отключиться от базы данных'
        myDialog.pushButton_Disconnect_RT.setEnabled(False)
        if States.Connected_RT:
            # Снимаем курсор
            ServerNames.seekRT.close()
            # Отключаемся от базы данных
            ServerNames.cnxnRT.close()
            States.Connected_RT = False
        # Переключаем в исходное состояние
        UpdateAirPortsSourcesChoiceByStatesAndFlags()
        myDialog.pushButton_Connect_RT.setEnabled(True)

    def PushButtonConnect_ACFN():
        if Flags.useAirCraftsDSN:
            myDialog.pushButton_Connect_AC.setEnabled(False)
            if not States.Connected_AC_XML:
                # Подключаемся к базе данных самолетов
                # todo Схема по умолчанию - dbo, другая схема указывается в явном виде
                ChoiceDSN_AC_XML = myDialog.comboBox_DSN_AC.currentText()
                # Добавляем атрибут myDSN
                ServerNames.myDSN_AC_XML = str(ChoiceDSN_AC_XML)
                try:
                    # через DSN + клиентский API-курсор (все настроено и протестировано в DSN)
                    ServerNames.cnxnAC_XML = pyodbc.connect("DSN=" + ServerNames.myDSN_AC_XML)
                    # Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде, в СУБД по умолчанию FALSE
                    ServerNames.cnxnAC_XML.autocommit = False
                    # Делаем свой экземпляр и ставим набор курсоров
                    # КУРСОР нужен для перехода функционального языка формул на процедурный или для вставки процедурных кусков в функциональный скрипт.
                    #
                    # Способы реализации курсоров:
                    #  - SQL, Transact-SQL,
                    #  - серверные API-курсоры (OLE DB, ADO, ODBC),
                    #  - клиентские API-курсоры (выборка кэшируется на клиенте)
                    #
                    # API-курсоры ODBC по SQLSetStmtAttr:
                    #  - тип SQL_ATTR_CURSOR_TYPE:
                    #    - однопроходный (последовательный доступ),
                    #    - статический (копия в tempdb),
                    #    - управляемый набор ключей,
                    #    - динамический,
                    #    - смешанный
                    #  - режим работы в стиле ISO:
                    #    - прокручиваемый SQL_ATTR_CURSOR_SCROLLABLE,
                    #    - обновляемый (чувствительный) SQL_ATTR_CURSOR_SENSITIVITY

                    # Клиентские однопроходные , статические API-курсоры ODBC.
                    # Добавляем атрибуты seek...
                    ServerNames.seekAC_XML = ServerNames.cnxnAC_XML.cursor()
                    States.Connected_AC_XML = True
                    # Переключаем в рабочее состояние
                    # SQL Server
                    myDialog.lineEdit_Server_remote.setEnabled(True)
                    myDialog.lineEdit_Server_remote.setText(ServerNames.cnxnAC_XML.getinfo(pyodbc.SQL_SERVER_NAME))
                    # Драйвер
                    myDialog.lineEdit_Driver_AC.setEnabled(True)
                    myDialog.lineEdit_Driver_AC.setText(ServerNames.cnxnAC_XML.getinfo(pyodbc.SQL_DRIVER_NAME))
                    # версия ODBC
                    myDialog.lineEdit_ODBCversion_AC.setEnabled(True)
                    myDialog.lineEdit_ODBCversion_AC.setText(ServerNames.cnxnAC_XML.getinfo(pyodbc.SQL_ODBC_VER))
                    # Схема (если из-под другой учетки, то выводит имя учетки)
                    myDialog.lineEdit_Schema_AC.setEnabled(True)
                    myDialog.lineEdit_Schema_AC.setText(ServerNames.cnxnAC_XML.getinfo(pyodbc.SQL_USER_NAME))
                    # Источник данных
                    myDialog.lineEdit_DSN_AC.setEnabled(True)
                    myDialog.lineEdit_DSN_AC.setText(ServerNames.cnxnAC_XML.getinfo(pyodbc.SQL_DATA_SOURCE_NAME))
                    # Переводим в рабочее состояние (продолжение)
                    UpdateFlightsSourcesChoiceByStatesAndFlags()
                    myDialog.pushButton_Disconnect_AC.setEnabled(True)
                except Exception:
                    myDialog.pushButton_Connect_AC.setEnabled(True)
                    message = QtWidgets.QMessageBox()
                    message.setText("Нет подключения к БД самолетов")
                    message.setIcon(QtWidgets.QMessageBox.Warning)
                    message.exec_()
                else:
                    pass
                finally:
                    pass
        else:
            myDialog.pushButton_Connect_AC.setEnabled(False)
            if not States.Connected_ACFN:
                # Подключаемся к базе данных авиаперелетов
                # todo Схема по умолчанию - dbo, другая схема указывается в явном виде
                ChoiceDB_ACFN = myDialog.comboBox_DB_FN.currentText()
                ChoiceDriver_ACFN = myDialog.comboBox_Driver_FN.currentText()
                # Добавляем атрибуты DataBase, DriverODBC
                ServerNames.DataBase_ACFN = str(ChoiceDB_ACFN)
                ServerNames.DriverODBC_ACFN = str(ChoiceDriver_ACFN)
                ChoiceDSN_ACFN = myDialog.comboBox_DSN_FN.currentText()
                # Добавляем атрибут myDSN
                ServerNames.myDSN_ACFN = str(ChoiceDSN_ACFN)
                try:
                    # Добавляем атрибут cnxn
                    if Flags.useAirFlightsDB:
                        # через драйвер СУБД + клиентский API-курсор
                        ServerNames.cnxnAC = pyodbc.connect(driver=ServerNames.DriverODBC_ACFN, server=ServerNames.ServerNameFlights, database=ServerNames.DataBase_ACFN)
                        ServerNames.cnxnFN = pyodbc.connect(driver=ServerNames.DriverODBC_ACFN, server=ServerNames.ServerNameFlights, database=ServerNames.DataBase_ACFN)
                    else:
                        # через DSN + клиентский API-курсор (все настроено и протестировано в DSN)
                        ServerNames.cnxnAC = pyodbc.connect("DSN=" + ServerNames.myDSN_ACFN)
                        ServerNames.cnxnFN = pyodbc.connect("DSN=" + ServerNames.myDSN_ACFN)
                    # Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде, в СУБД по умолчанию FALSE
                    ServerNames.cnxnAC.autocommit = False
                    ServerNames.cnxnFN.autocommit = False
                    # Делаем свой экземпляр и ставим набор курсоров
                    # КУРСОР нужен для перехода функционального языка формул на процедурный или для вставки процедурных кусков в функциональный скрипт.
                    #
                    # Способы реализации курсоров:
                    #  - SQL, Transact-SQL,
                    #  - серверные API-курсоры (OLE DB, ADO, ODBC),
                    #  - клиентские API-курсоры (выборка кэшируется на клиенте)
                    #
                    # API-курсоры ODBC по SQLSetStmtAttr:
                    #  - тип SQL_ATTR_CURSOR_TYPE:
                    #    - однопроходный (последовательный доступ),
                    #    - статический (копия в tempdb),
                    #    - управляемый набор ключей,
                    #    - динамический,
                    #    - смешанный
                    #  - режим работы в стиле ISO:
                    #    - прокручиваемый SQL_ATTR_CURSOR_SCROLLABLE,
                    #    - обновляемый (чувствительный) SQL_ATTR_CURSOR_SENSITIVITY

                    # Клиентские однопроходные , статические API-курсоры ODBC.
                    # Добавляем атрибуты seek...
                    ServerNames.seekAC = ServerNames.cnxnAC.cursor()
                    ServerNames.seekFN = ServerNames.cnxnFN.cursor()
                    States.Connected_ACFN = True
                    # Переключаем в рабочее состояние
                    # SQL Server
                    myDialog.lineEdit_Server_remote.setEnabled(True)
                    myDialog.lineEdit_Server_remote.setText(ServerNames.cnxnFN.getinfo(pyodbc.SQL_SERVER_NAME))
                    # Драйвер
                    myDialog.lineEdit_Driver_AC.setEnabled(True)
                    myDialog.lineEdit_Driver_AC.setText(ServerNames.cnxnFN.getinfo(pyodbc.SQL_DRIVER_NAME))
                    # Версия ODBC
                    myDialog.lineEdit_ODBCversion_AC.setEnabled(True)
                    myDialog.lineEdit_ODBCversion_AC.setText(ServerNames.cnxnFN.getinfo(pyodbc.SQL_ODBC_VER))
                    # Схема (если из-под другой учетки, то выводит имя учетки)
                    myDialog.lineEdit_Schema_AC.setEnabled(True)
                    myDialog.lineEdit_Schema_AC.setText(ServerNames.cnxnFN.getinfo(pyodbc.SQL_USER_NAME))
                    # Источник данных
                    myDialog.lineEdit_DSN_AC.setEnabled(True)
                    myDialog.lineEdit_DSN_AC.setText(ServerNames.cnxnFN.getinfo(pyodbc.SQL_DATA_SOURCE_NAME))
                    # Переводим в рабочее состояние (продолжение)
                    UpdateFlightsSourcesChoiceByStatesAndFlags()
                    if States.Connected_AL and States.Connected_RT:
                        PrepareForInputData(True)
                    myDialog.pushButton_Disconnect_AC.setEnabled(True)
                except Exception:
                    myDialog.pushButton_Connect_AC.setEnabled(True)
                    message = QtWidgets.QMessageBox()
                    message.setText("Нет подключения к БД авиаперелетов")
                    message.setIcon(QtWidgets.QMessageBox.Warning)
                    message.exec_()
                else:
                    pass
                finally:
                    pass

    def PushButtonDisconnect_ACFN():
        # Обработчик кнопки 'Отключиться от базы данных'
        myDialog.pushButton_Disconnect_AC.setEnabled(False)
        if States.Connected_AC_XML:
            # Снимаем курсор
            ServerNames.seekAC_XML.close()
            # Отключаемся от базы данных
            ServerNames.cnxnAC_XML.close()
            States.Connected_AC_XML = False
        if States.Connected_ACFN:
            # Снимаем курсор
            ServerNames.seekAC.close()
            # Отключаемся от базы данных
            ServerNames.cnxnAC.close()
            States.Connected_AC = False
            # Снимаем курсор
            ServerNames.seekFN.close()
            # Отключаемся от базы данных
            ServerNames.cnxnFN.close()
            States.Connected_ACFN = False
        UpdateFlightsSourcesChoiceByStatesAndFlags()
        myDialog.pushButton_Connect_AC.setEnabled(True)


    def PushButtonChooseCSVFile():
        filter = "Data files (*.csv)"
        FileNames.InputFileCSV = QtWidgets.QFileDialog.getOpenFileName(None, "Открыть рабочие данные", ' ', filter=filter)[0]
        urnCSV = FileNames.InputFileCSV.rstrip(os.sep)  # не сработало
        filenameCSV = pathlib.Path(FileNames.InputFileCSV).name  # сработало
        myDialog.lineEdit_CSVFile.setText(filenameCSV)

    def PushButtonChooseTXTFile():
        filter = "Log Files (*.txt *.text)"
        FileNames.LogFileTXT = QtWidgets.QFileDialog.getOpenFileName(None, "Открыть журнал", ' ', filter=filter)[0]
        filenameTXT = pathlib.Path(FileNames.LogFileTXT).name
        myDialog.lineEdit_TXTFile.setText(filenameTXT)

    def QueryAirLineByIATA(iata):
        # Возвращает строку авиакомпании по ее коду IATA
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            ServerNames.seekAL.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA = '" + str(iata) + "' "
            ServerNames.seekAL.execute(SQLQuery)
            ResultSQL = ServerNames.seekAL.fetchone()
            ServerNames.cnxnAL.commit()
        except Exception:
            ResultSQL = False
            ServerNames.cnxnAL.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def QueryAirCraftByRegistration(Registration, useAirCrafts):
        # Возвращает строку самолета по его регистрации
        if useAirCrafts:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
                ServerNames.seekAC_XML.execute(SQLQuery)
                SQLQuery = "SELECT * FROM dbo.AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = '" + str(Registration) + "' "
                ServerNames.seekAC_XML.execute(SQLQuery)
                ResultSQL = ServerNames.seekAC_XML.fetchone()  # курсор забирает одну строку и сдвигается на строку вниз
                ServerNames.cnxnAC_XML.commit()
            except Exception:
                ResultSQL = False
                ServerNames.cnxnAC_XML.rollback()
        else:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
                ServerNames.seekAC.execute(SQLQuery)
                SQLQuery = "SELECT * FROM dbo.AirCraftsTable WHERE AirCraftRegistration = '" + str(Registration) + "' "
                ServerNames.seekAC.execute(SQLQuery)
                ResultSQL = ServerNames.seekAC.fetchone()  # курсор забирает одну строку и сдвигается на строку вниз
                ServerNames.cnxnAC.commit()
            except Exception:
                ResultSQL = False
                ServerNames.cnxnAC.rollback()
        return ResultSQL

    def InsertAirCraftByRegistration(Registration, ALPK, useAirCrafts):
        if useAirCrafts:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
                ServerNames.seekAC_XML.execute(SQLQuery)
                SQLQuery = "INSERT INTO dbo.AirCraftsTableNew2XsdIntermediate (AirCraftRegistration) VALUES ('"
                SQLQuery += str(Registration) + "') "
                ServerNames.seekAC_XML.execute(SQLQuery)  # записываем данные по самолету в БД
                # todo Дописать авиакомпанию-оператора в поле AirFlightsByAirLines -> не надо (он в начале FlightNumberString)
                ResultSQL = True
                ServerNames.cnxnAC_XML.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
            except Exception:
                ResultSQL = False
                ServerNames.cnxnAC_XML.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
        else:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
                ServerNames.seekAC.execute(SQLQuery)
                if ALPK is None:
                    SQLQuery = "INSERT INTO dbo.AirCraftsTable (AirCraftRegistration) VALUES ('"
                    SQLQuery += str(Registration) + "') "
                else:
                    SQLQuery = "INSERT INTO dbo.AirCraftsTable (AirCraftRegistration, AirCraftAirLine) VALUES ('"
                    SQLQuery += str(Registration) + "', "
                    SQLQuery += str(ALPK) + ") "
                ServerNames.seekAC.execute(SQLQuery)  # записываем данные по самолету в БД
                ResultSQL = True
                ServerNames.cnxnAC.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
            except Exception:
                ResultSQL = False
                ServerNames.cnxnAC.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
        return ResultSQL

    def QueryAirLineByPK(pk):
        # Возвращает строку авиакомпании по первичному ключу
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            ServerNames.seekAL.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineUniqueNumber = '" + str(pk) + "' "
            ServerNames.seekAL.execute(SQLQuery)
            ResultSQL = ServerNames.seekAL.fetchone()
            ServerNames.cnxnAL.commit()
        except Exception:
            ResultSQL = False
            ServerNames.cnxnAL.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def UpdateAirCraft(Registration, ALPK, useAirCrafts):
        if useAirCrafts:
            return True
        else:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
                ServerNames.seekAC.execute(SQLQuery)
                SQLQuery = "UPDATE dbo.AirCraftsTable SET AirCraftAirLine = " + str(ALPK) + " WHERE AirCraftRegistration = '" + str(Registration) + "' "
                ServerNames.seekAC.execute(SQLQuery)  # записываем данные по самолету в БД
                ResultSQL = True
                ServerNames.cnxnAC.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
            except Exception:
                ResultSQL = False
                ServerNames.cnxnAC.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
            else:
                pass
            finally:
                return ResultSQL

    def QueryAirRoute(IATADeparture, IATAArrival):
        # Возвращает строку маршрута по кодам IATA аэропортов
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            ServerNames.seekRT.execute(SQLQuery)
            SQLQuery = """SELECT dbo.AirRoutesTable.AirRouteUniqueNumber                                 
                       FROM dbo.AirRoutesTable INNER JOIN
                       dbo.AirPortsTable ON dbo.AirRoutesTable.AirPortDeparture = dbo.AirPortsTable.AirPortUniqueNumber INNER JOIN
                       dbo.AirPortsTable AS AirPortsTable_1 ON dbo.AirRoutesTable.AirPortArrival = AirPortsTable_1.AirPortUniqueNumber
                       WHERE (dbo.AirPortsTable.AirPortCodeIATA = '""" + str(IATADeparture) + "') AND (AirPortsTable_1.AirPortCodeIATA = '" + str(IATAArrival) + "') "
            ServerNames.seekRT.execute(SQLQuery)
            ResultSQL = ServerNames.seekRT.fetchone()
            ServerNames.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            ServerNames.cnxnRT.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def InsertAirRoute(IATADeparture, IATAArrival):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            ServerNames.seekRT.execute(SQLQuery)
            SQLQuery = "INSERT INTO dbo.AirRoutesTable (AirPortDeparture, AirPortArrival) VALUES ("
            SQLQuery += str(IATADeparture) + ", "  # bigint
            SQLQuery += str(IATAArrival) + ") "  # bigint
            ServerNames.seekRT.execute(SQLQuery)
            ResultSQL = True
            ServerNames.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            ServerNames.cnxnRT.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def InsertAirPortByIATA(iata):
        # fixme дописать функционал, когда код пустой
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            ServerNames.seekRT.execute(SQLQuery)
            SQLQuery = "INSERT INTO dbo.AirPortsTable (AirPortCodeIATA) VALUES ('" + str(iata) + "') "
            ServerNames.seekRT.execute(SQLQuery)
            ResultSQL = True
            ServerNames.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            ServerNames.cnxnRT.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def ModifyAirFlight(ac, al, fn, dep, arr, flightdate, begindate, useAirCrafts, useXQuery):

        class Results:
            Result = False  # Коды возврата: 0 - несработка, 1 - вставили, 2 - сплюсовали

        db_air_route = QueryAirRoute(dep, arr).AirRouteUniqueNumber
        if db_air_route is not None:
            db_air_craft = QueryAirCraftByRegistration(ac, useAirCrafts).AirCraftUniqueNumber
            if db_air_craft is not None:
                if useAirCrafts:
                    if useXQuery:
                        try:
                            SQLQuery = "DECLARE @ReturnData INT = 5 "
                            #SQLQuery += "SET @ReturnData = 5 "
                            #self.seekAC_XML.execute(SQLQuery)
                            SQLQuery = "EXECUTE dbo.SPUpdateFlightsByRoutes '" + str(ac) + "', '" + str(al) + str(fn) + "Test" + "', " + str(db_air_route) + ", '" + str(flightdate) + "', '" + str(begindate) + "' "
                            ServerNames.seekAC_XML.execute(SQLQuery)
                            #SQLQuery = "SELECT @ReturnData "
                            #self.seekAC_XML.execute(SQLQuery)
                            Data = ServerNames.seekAC_XML.fetchall()  # fetchval() - pyodbc convenience method similar to cursor.fetchone()[0]
                            print("Data = " + str(Data))
                            if Data:
                                Results.Result = Data[0]
                            else:
                                Results.Result = 1
                            print(" Результат хранимой процедуры = " + str(Results.Result))
                            #self.seekAC_XML.callproc('dbo.SPUpdateFlightsByRoutes', (ac, al + fn, db_air_route, flightdate, begindate))
                            #Status = self.seekAC_XML.proc_status
                            #print(" Status = " + str(Status))
                            ServerNames.cnxnAC_XML.commit()
                        except pyodbc.Error as error:
                            sqlstate0 = error.args[0]
                            sqlstate1 = error.args[1]
                            print(" pyodbcError = " + str(sqlstate0.split(".")) + " , " + str(sqlstate1))
                            ServerNames.cnxnAC_XML.rollback()
                            Results.Result = 0
                        except Exception as exception:
                            print(" exception = " + str(exception))
                            ServerNames.cnxnAC_XML.rollback()
                            Results.Result = 0
                    else:
                        # fixme на первых 5-ти загрузках файл журнала стал в 1000 раз больше файла данных (модель восстановления БД - ПОЛНАЯ) -> сделал ПРОСТАЯ
                        try:
                            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
                            ServerNames.seekAC_XML.execute(SQLQuery)
                            XMLQuery = "SELECT FlightsByRoutes FROM dbo.AirCraftsTableNew2XsdIntermediate WITH (UPDLOCK) WHERE AirCraftRegistration = '" + str(ac) + "' "
                            ServerNames.seekAC_XML.execute(XMLQuery)
                            ResultXML = ServerNames.seekAC_XML.fetchone()
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
                            ServerNames.seekAC_XML.execute(XMLQuery)
                            ServerNames.cnxnAC_XML.commit()
                        except Exception:
                            ServerNames.cnxnAC_XML.rollback()
                            Results.Result = 0
                else:
                    try:
                        SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
                        ServerNames.seekFN.execute(SQLQuery)
                        SQLQuery = "SELECT * FROM dbo.AirFlightsTable WITH (UPDLOCK) WHERE FlightNumberString = '" + str(al) + str(fn) + "' AND AirRoute = "
                        SQLQuery += str(db_air_route) + " AND AirCraft = " + str(db_air_craft) + " AND FlightDate = '" + str(flightdate) + "' AND BeginDate = '" + str(begindate) + "' "
                        ServerNames.seekFN.execute(SQLQuery)
                        ResultQuery = ServerNames.seekFN.fetchone()
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
                        ServerNames.seekFN.execute(SQLQuery)
                        ServerNames.cnxnFN.commit()
                    except Exception:
                        ServerNames.cnxnFN.rollback()
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

    def QueryAirPortByIATA(iata):
        # Возвращает строку аэропорта по коду IATA
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            ServerNames.seekRT.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeIATA = '" + str(iata) + "' "
            ServerNames.seekRT.execute(SQLQuery)
            ResultSQL = ServerNames.seekRT.fetchone()
            ServerNames.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            ServerNames.cnxnRT.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def InsertAirLineByIATAandICAO(iata, icao):
        # Вставляем авиакомпанию с кодами IATA и ICAO, альянсом по умолчанию
        # fixme Потом подправить Альанс авиакомпании
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            ServerNames.seekAL.execute(SQLQuery)
            if iata is None:
                print(" ICAO=", str(icao))
                SQLQuery = "INSERT INTO dbo.AirLinesTable (AirLineCodeICAO) VALUES ('" + str(icao) + "') "
            elif icao is None:
                print(" IATA=", str(iata))
                SQLQuery = "INSERT INTO dbo.AirLinesTable (AirLineCodeIATA) VALUES ('" + str(iata) + "') "
            elif iata is None and icao is None:
                print(" IATA=", str(iata), " ICAO=", str(icao))
                SQLQuery = "INSERT INTO dbo.AirLinesTable (AirLineCodeIATA, AirLineCodeICAO) VALUES (NULL, NULL) "
                #print("raise Exception")
                #raise Exception
            else:
                print(" IATA=", str(iata), " ICAO=", str(icao))
                SQLQuery = "INSERT INTO dbo.AirLinesTable (AirLineCodeIATA, AirLineCodeICAO) VALUES ('" + str(iata) + "', '" + str(icao) + "') "
            ServerNames.seekAL.execute(SQLQuery)  # записываем данные по самолету в БД
            ResultSQL = True
            ServerNames.cnxnAL.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
        except Exception:
            ResultSQL = False
            ServerNames.cnxnAL.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
        else:
            pass
        finally:
            return ResultSQL

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
        if Flags.SetInputDate:
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
                DBAirLine = QueryAirLineByIATA(AL)
                if DBAirLine is None:
                    if InsertAirLineByIATAandICAO(AL, None):
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
                DBAirCraft = QueryAirCraftByRegistration(AC, Flags.useAirCraftsDSN)
                if DBAirCraft is None:
                    DBAirLine = QueryAirLineByIATA(AL)
                    if DBAirLine is None:
                        # Вставляем самолет с пустым внешним ключем
                        if InsertAirCraftByRegistration(Registration=AC, ALPK=None, useAirCrafts=Flags.useAirCraftsDSN):
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
                        if InsertAirCraftByRegistration(Registration=AC, ALPK=DBAirLine.AirLineUniqueNumber, useAirCrafts=Flags.useAirCraftsDSN):
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
                    if Flags.useAirCraftsDSN:
                        break
                    else:
                        DBAirLinePK = QueryAirLineByPK(DBAirCraft.AirCraftAirLine)
                        if DBAirLinePK is None or DBAirLinePK.AirLineCodeIATA != AL:
                            # fixme пустая ячейка в таблице SQL-ной БД - NULL <-> в Python-е - (None,) -> в условиях None и (None,) - не False и не True
                            # fixme Просмотрел таблицу самолетов скриптом на SQL -> регистрация UNKNOWN не имеет внешнего ключа авиакомпании
                            # fixme Просмотрел таблицу самолетов скриптом на SQL -> регистрация nan каждый раз переписывается на другую компанию-оператора
                            DBAirLine = QueryAirLineByIATA(AL)
                            if DBAirLine is None:
                                break
                            elif DBAirLine is not None:
                                if UpdateAirCraft(Registration=AC, ALPK=DBAirLine.AirLineUniqueNumber, useAirCrafts=Flags.useAirCraftsDSN):
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
                DBAirPortDep = QueryAirPortByIATA(Dep)
                if DBAirPortDep is not None:
                    DBAirPortArr = QueryAirPortByIATA(Arr)
                    if DBAirPortArr is not None:
                        DBAirRoute = QueryAirRoute(Dep, Arr)
                        if DBAirRoute is None:
                            # Если есть оба аэропорта и нет маршрута
                            if InsertAirRoute(DBAirPortDep.AirPortUniqueNumber, DBAirPortArr.AirPortUniqueNumber):
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
                        if InsertAirPortByIATA(Arr):
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
                    if InsertAirPortByIATA(Dep):
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
            if not Flags.SetInputDate:
                FD = Flags.BeginDate
            # Цикл попыток
            for attemptNumber in range(attemptRetryCount):
                deadlockCount = attemptNumber
                DBAirLine = QueryAirLineByIATA(AL)
                if DBAirLine is not None:
                    DBAirCraft = QueryAirCraftByRegistration(AC, useAirCraftsDSN)
                    if DBAirCraft is not None:
                        DBAirRoute = QueryAirRoute(Dep, Arr)
                        if DBAirRoute is not None:
                            # todo между транзакциями маршрут и самолет еще раз перезапросить внутри вызываемой функции - СДЕЛАЛ
                            ResultModify = ModifyAirFlight(AC, AL, FN, Dep, Arr, FD, S.BeginDate, useAirCraftsDSN, useXQuery)
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
        OutputString += " Источник входных данных = " + str(FileNames.InputFileCSV) + " \n"
        OutputString += " Входные данные внесены за " + str(Flags.BeginDate) + " \n"
        if Flags.SetInputDate:
            OutputString += " Дата авиарейса проставлена из входного файла\n"
        else:
            OutputString += " Дата авиарейса проставлена как 1-ое число указанного месяца \n"
        if Flags.useXQuery:
            OutputString += " Используется xQuery (SAX) \n"
        else:
            OutputString += " Используется xml.etree.ElementTree (DOM) \n"
        if Flags.useAirCraftsDSN:
            OutputString += " Сервер СУБД = " + str(ServerNames.cnxnAC_XML.getinfo(pyodbc.SQL_SERVER_NAME)) + " \n"
            OutputString += " Драйвер = " + str(ServerNames.cnxnAC_XML.getinfo(pyodbc.SQL_DRIVER_NAME)) + " \n"
            OutputString += " Версия ODBC = " + str(ServerNames.cnxnAC_XML.getinfo(pyodbc.SQL_ODBC_VER)) + " \n"
            OutputString += " DSN = " + str(ServerNames.cnxnAC_XML.getinfo(pyodbc.SQL_DATA_SOURCE_NAME)) + " \n"
            OutputString += " Схема = " + str(ServerNames.cnxnAC_XML.getinfo(pyodbc.SQL_USER_NAME)) + " \n"
        else:
            OutputString += " Сервер СУБД = " + str(ServerNames.cnxnFN.getinfo(pyodbc.SQL_SERVER_NAME)) + " \n"
            OutputString += " Драйвер = " + str(ServerNames.cnxnFN.getinfo(pyodbc.SQL_DRIVER_NAME)) + " \n"
            OutputString += " Версия ODBC = " + str(ServerNames.cnxnFN.getinfo(pyodbc.SQL_ODBC_VER)) + " \n"
            OutputString += " DSN = " + str(ServerNames.cnxnFN.getinfo(pyodbc.SQL_DATA_SOURCE_NAME)) + " \n"
            OutputString += " Схема = " + str(ServerNames.cnxnFN.getinfo(pyodbc.SQL_USER_NAME)) + " \n"
        OutputString += " Длительность загрузки = " + str(EndTime - StartTime) + " \n"
        OutputString += " Пользователь = " + str(os.getlogin()) + " \n"
        OutputString += " Итоги: \n"
        # Формируем итоги
        # todo Сделать итоги в виде XML и писать его полем XML.Document в базу данных
        if ListAirLinesAdded:
            OutputString += " - вставились авиакомпании: \n  "
            OutputString += str(set(ListAirLinesAdded))  # fixme с регистрациями NaN надолго зависает, не убирает повторы и не группирует
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
        # fixme Большая строка не дописывается, скрипт долго висит
        try:
            # fixme При больших объемах дозаписи и одновременном доступе к журналу нескольких обработок не все результаты дописываются в него
            LogFile = open(Log, 'a')
            LogFile.write(OutputString)
            # LogFile.write('Вывод обычным способом\n')
        except IOError:
            try:
                LogError = open(FileNames.ErrorFileTXT, 'a')
                LogError.write("Ошибка дозаписи результатов по " + str(FileNames.InputFileCSV) + " в " + str(FileNames.InputFileCSV) + " \n")
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
        myDialog.label_22.setStyleSheet("border: 5px solid; border-color: pink")  # fixme Тут графическая оболочка слетела -> Задержка не дала результат
        print(termcolor.colored("Загрузка окончена", "red", "on_yellow"))
        # Снимаем курсоры
        ServerNames.seekAL.close()
        ServerNames.seekRT.close()
        if Flags.useAirCraftsDSN:
            ServerNames.seekAC_XML.close()
        else:
            ServerNames.seekAC.close()
            ServerNames.seekFN.close()
        # Отключаемся от баз данных
        ServerNames.cnxnAL.close()
        ServerNames.cnxnRT.close()
        if Flags.useAirCraftsDSN:
            ServerNames.cnxnAC_XML.close()
        else:
            ServerNames.cnxnAC.close()
            ServerNames.cnxnFN.close()

    def PushButtonGetStarted():
        myDialog.pushButton_GetStarted.setEnabled(False)
        Flags.BeginDate = myDialog.dateEdit_BeginDate.date().toString('yyyy-MM-dd')
        if myDialog.checkBox_SetInputDate.isChecked():
            S.SetInputDate = True
        else:
            S.SetInputDate = False
        myDialog.pushButton_ChooseCSVFile.setEnabled(False)
        myDialog.pushButton_ChooseTXTFile.setEnabled(False)
        myDialog.dateEdit_BeginDate.setEnabled(False)
        myDialog.checkBox_SetInputDate.setEnabled(False)
        myDialog.pushButton_Disconnect_AL.setEnabled(False)
        myDialog.pushButton_Disconnect_RT.setEnabled(False)
        myDialog.pushButton_Disconnect_AC.setEnabled(False)
        myDialog.label_execute.setEnabled(True)
        # todo Заброс на возможность запуска нескольких загрузок с доработкой графической оболочки без ее закрытия на запуске загрузки
        threadLoad = threading.Thread(target=LoadThread, daemon=False, args=(FileNames.InputFileCSV, FileNames.LogFileTXT, ))  # поток не сам по себе
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
