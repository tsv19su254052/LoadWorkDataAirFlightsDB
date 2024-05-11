#  Interpreter 3.7 -> 3.10


import pyodbc
import pymssql  # работает тяжелее
# todo Вероятно придется много переделать, чтобы не вызывать по 2 раза. Не работает с XML-ными полями см. https://docs.sqlalchemy.org/en/20/dialects/mssql.html#sqlalchemy.dialects.mssql.XML
from sqlalchemy import create_engine


# Делаем предков
class ServerExchange:
    def __init__(self, c, s):
        self.cnxn = c  # подключение
        self.seek = s  # курсор

    def connectDBodbc(self, driver, servername, database):
        self.Result = False
        try:
            # через драйвер СУБД + клиентский API-курсор
            self.cnxn = pyodbc.connect(driver=driver, server=servername, database=database)
            # Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде, в СУБД по умолчанию FALSE
            self.cnxn.autocommit = False
            # Делаем свой экземпляр и ставим курсор
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

            # Клиентский однопроходной, статический API-курсор ODBC.
            # Добавляем атрибут seek...
            self.seek = self.cnxn.cursor()
            self.Result = True
        except Exception:
            self.Result = False
        return self.Result

    def connectDBmssql(self, servername, database):
        self.Result = False
        try:
            # через драйвер СУБД + клиентский API-курсор
            # Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде
            #self.cnxn = pymssql.connect(server=servername, database=database, host=host, autocommit=False)
            self.cnxn = pymssql.connect(server=servername, database=database, autocommit=False)
            # Делаем свой экземпляр и ставим курсор
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

            # Клиентский однопроходной, статический API-курсор ODBC.
            # Добавляем атрибут seek...
            self.seek = self.cnxn.cursor()
            self.Result = True
        except Exception:
            self.Result = False
        return self.Result

    def connectDSNodbc(self, dsn):
        self.Result = False
        try:
            # через DSN + клиентский API-курсор (все настроено и протестировано в DSN)
            self.cnxn = pyodbc.connect("DSN=" + dsn)
            # Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде, в СУБД по умолчанию FALSE
            self.cnxn.autocommit = False
            # Делаем свой экземпляр и ставим курсор
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

            # Клиентский однопроходной, статический API-курсор ODBC.
            # Добавляем атрибут seek...
            self.seek = self.cnxn.cursor()
            self.Result = True
        except Exception:
            self.Result = False
        return self.Result

    def disconnect(self):
        try:
            # Снимаем курсор
            self.seek.close()
            # Отключаемся от базы данных
            self.cnxn.close()
            print(" -- БД отключена")
        except Exception:
            print(" -- БД уже отключена")

    def getSQLDrivers(self):
        SQLDrivers = pyodbc.drivers()
        return SQLDrivers

    def getDataSources(self):
        DataSources = pyodbc.dataSources()
        return DataSources

    def getSQLDataODBC(self):
        SQLData = (self.cnxn.getinfo(pyodbc.SQL_SERVER_NAME),
                   self.cnxn.getinfo(pyodbc.SQL_DRIVER_NAME),
                   self.cnxn.getinfo(pyodbc.SQL_ODBC_VER),
                   self.cnxn.getinfo(pyodbc.SQL_DATA_SOURCE_NAME),
                   self.cnxn.getinfo(pyodbc.SQL_USER_NAME))
        return SQLData

    def getSQLDatamssql(self):
        SQLData = (self.cnxn.getinfo(pymssql.STRING),
                   self.cnxn.getinfo(pymssql.paramstyle),
                   self.cnxn.getinfo(pymssql.VERSION),
                   self.cnxn.getinfo(pymssql.get_dbversion()),
                   self.cnxn.getinfo(pymssql.apilevel))
        return SQLData
