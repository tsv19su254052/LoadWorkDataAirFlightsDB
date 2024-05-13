#  Interpreter 3.7 -> 3.10


from xml.etree import ElementTree
# todo ветка библиотек Qt - QtCore, QtGui, QtNetwork, QtOpenGL, QtScript, QtSQL (медленнее чем pyodbc), QtDesigner, QtXml
# Руководство по установке см. https://packaging.python.org/tutorials/installing-packages/

# Пользовательская библиотека с классами
from modulesFilesWithClasses.moduleClassServerExchange import ServerExchange
# Задача создания пользовательских структур данных не расматривается -> Только функционал
# Компилируется и кладется в папку __pycache__
# Идея выноса каждого класса в этот отдельный файл, как на Java -> Удобство просмотра типов данных, не особо практично


class ServerNames:
    def __init__(self):
        # Имена серверов
        #self.ServerNameOriginal = "data-server-1.movistar.vrn.skylink.local"
        self.ServerNameOriginal = "localhost\mssqlserver15"  # указал имя NetBIOS и указал инстанс
        self.ServerHost = "localhost\mssqlserver15"
        #self.ServerNameOriginal = "localhost\sqldeveloper"  # указал инстанс
        # fixme Забыл отменить обратно, надо проверить как самолеты и авиарейсы грузились без него причем в рабочую базу -> Все нормально, этот выбор работал, если грузить не через системный DSN
        self.ServerNameFlights = "data-server-1.movistar.vrn.skylink.local"  # указал ресурсную запись из DNS
        self.ServerName = "localhost\mssqlserver15"  # указал инстанс
        #self.ServerName = "localhost\sqldeveloper"  # указал инстанс


class FileNames:
    def __init__(self):
        # Имена читаемых и записываемых файлов
        self.InputFileCSV = ' '
        self.LogFileTXT = ' '
        self.ErrorFileTXT = 'LogReport_Errors.txt'


class Flags:
    def __init__(self):
        # Флаги
        self.useAirCrafts = False
        self.useAirFlightsDB = True
        self.useAirCraftsDB = True
        self.useXQuery = False
        self.useMSsql = False
        self.useODBCMarkers = False
        self.SetInputDate = False
        self.BeginDate = ' '


class States:
    def __init__(self):
        # Состояния
        self.Connected_AL = False
        self.Connected_RT = False
        self.Connected_ACFN = False
        self.Connected_AC = False


SE = ServerExchange


class ACFN(SE):
    def __init__(self):
        super().__init__(c=None, s=None)
        # AirLine
        self.AirLine_ID = 1
        self.AirLineName = " "
        self.AirLineAlias = " "
        self.AirLineCodeIATA = " "
        self.AirLineCodeICAO = " "
        self.AirLineCallSighn = " "
        self.AirLineCity = " "
        self.AirLineCountry = " "
        self.AirLineStatus = 1
        self.CreationDate = '1990-01-01'
        self.AirLineDescription = " "
        self.Alliance = 4
        self.Position = 1  # Позиция курсора в таблице (в SQL начинается с 1)
        self.cnxn_AL_odbc = None  # подключение
        self.seek_AL_odbc = None  # курсор

        # AirCraft
        self.AirCraftModel = 387  # Unknown Model
        self.BuildDate = '1990-01-01'
        self.RetireDate = '1990-01-01'
        self.AirCraftSourceCSVFile = " "
        self.AirCraftDescription = " "
        self.AirCraftLineNumber_LN = " "
        self.AirCraftLineNumber_MSN = " "
        self.AirCraftSerialNumber_SN = " "
        self.AirCraftCNumber = " "
        self.EndDate = '1990-01-01'
        # Подключения
        self.cnxn_AC_mssql = None
        self.cnxn_AC_odbc = None
        self.cnxn_ACFN_odbc = None
        # Курсоры
        self.seek_AC_mssql = None
        self.seek_AC_odbc = None
        self.seek_ACFN_odbc = None

        # AirPort
        self.HyperLinkToWikiPedia = " "
        self.HyperLinkToAirPortSite = " "
        self.HyperLinkToOperatorSite = " "
        self.HyperLinksToOtherSites = " "
        self.AirPortCodeIATA = " "
        self.AirPortCodeICAO = " "
        self.AirPortCodeFAA_LID = " "
        self.AirPortCodeWMO = " "
        self.AirPortName = " "
        self.AirPortCity = " "
        self.AirPortCounty = " "
        self.AirPortCountry = " "
        self.AirPortLatitude = 0
        self.AirPortLongitude = 0
        self.HeightAboveSeaLevel = 0
        self.SourceCSVFile = " "
        self.AirPortDescription = " "
        self.AirPortRunWays = " "
        self.AirPortFacilities = " "
        self.AirPortIncidents = " "
        self.cnxn_RT_odbc = None  # подключение
        self.seek_RT_odbc = None  # курсор
        self.LogCountViewed = 0
        self.LogCountChanged = 0

    def getListDataBasesLocal(self):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_AL_odbc.execute(SQLQuery)
            SQLQuery = "SELECT name from sys.databases"
            self.seek_AL_odbc.execute(SQLQuery)
            ResultSQL = self.seek_AL_odbc.fetchall()
            self.cnxn_AL_odbc.commit()
            print(" результат запроса = " + str(ResultSQL))
            #список баз данных = [('master',), ('tempdb',), ('model',), ('msdb',), ('AirCraftsDBNew62',), ('AirLinesDBNew62',), ('AirPortsAndRoutesDBNew62',)]
            ListDataBases = []
            ListDataBasesAirLines = []
            ListDataBasesAirCrafts = []
            ListDataBasesAirPorts = []
            for line in ResultSQL:
                print(" line = " + str(line[0]))
                if line[0] != 'master' and line[0] != 'tempdb' and line[0] != 'model' and line[0] != 'msdb':
                    ListDataBases.append(line[0])
            print(" список баз = " + str(ListDataBases))
            for string in ListDataBases:
                if 'AirLines' in string:
                    ListDataBasesAirLines.append(string)
                if 'AirCrafts' in string:
                    ListDataBasesAirCrafts.append(string)
                if 'AirPorts' in string:
                    ListDataBasesAirPorts.append(string)
            print(" БД авиакомпаний = " + str(ListDataBasesAirLines))
            print(" БД самолетов = " + str(ListDataBasesAirCrafts))
            print(" БД аэропортов = " + str(ListDataBasesAirPorts))
        except Exception:
            ResultSQL = False
            self.cnxn_AL_odbc.rollback()
        return ListDataBases

    def getListDataBasesRemote(self):
        pass

    class AirLine:
        def __init__(self):
            pass

    def connectDB_AL_odbc(self, servername, driver, database):
        if self.connectDB_odbc(servername=servername, driver=driver, database=database):
            self.cnxn_AL_odbc = self.cnxn
            self.seek_AL_odbc = self.seek
            self.getListDataBasesLocal()
            return True
        else:
            return False

    def disconnectAL_odbc(self):
        try:
            # Закрываем курсор
            self.seek_AL_odbc.close()
            # Отключаемся от базы данных
            self.cnxn_AL_odbc.close()
            print(" -- БД отключена")
        except Exception:
            print(" -- БД уже отключена")
        #self.disconnect()

    def QueryAlliances(self):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_AL_odbc.execute(SQLQuery)
            SQLQuery = "SELECT AllianceUniqueNumber, AllianceName FROM dbo.AlliancesTable"  # Убрал  ORDER BY AlianceName
            self.seek_AL_odbc.execute(SQLQuery)
            ResultSQL = self.seek_AL_odbc.fetchall()
            self.cnxn_AL_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_AL_odbc.rollback()
        return ResultSQL

    def QueryAlliancesSqlAlchemy(self):
        pass

    def QueryAlliancePKByName(self, name):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_AL_odbc.execute(SQLQuery)
            SQLQuery = "SELECT AllianceUniqueNumber FROM dbo.AlliancesTable WHERE AllianceName='" + str(name) + "' "  # Убрал  ORDER BY AlianceName
            self.seek_AL_odbc.execute(SQLQuery)
            ResultSQL = self.seek_AL_odbc.fetchone()
            self.cnxn_AL_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_AL_odbc.rollback()
        return ResultSQL[0]

    def QueryAirLineByPK(self, pk):
        # Возвращает строку авиакомпании по первичному ключу
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_AL_odbc.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineUniqueNumber = '" + str(pk) + "' "
            self.seek_AL_odbc.execute(SQLQuery)
            ResultSQL = self.seek_AL_odbc.fetchone()
            self.cnxn_AL_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_AL_odbc.rollback()
        return ResultSQL

    def QueryAirLineByIATA(self, iata):
        # Возвращает строку авиакомпании по ее коду IATA
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_AL_odbc.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA = '" + str(iata) + "' "
            self.seek_AL_odbc.execute(SQLQuery)
            ResultSQL = self.seek_AL_odbc.fetchone()
            self.cnxn_AL_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_AL_odbc.rollback()
        return ResultSQL

    def QueryAirLineByICAO(self, icao):
        # Возвращает строку авиакомпании по ее коду ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_AL_odbc.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeICAO = '" + str(icao) + "' "
            self.seek_AL_odbc.execute(SQLQuery)
            ResultSQL = self.seek_AL_odbc.fetchone()
            self.cnxn_AL_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_AL_odbc.rollback()
        return ResultSQL

    def QueryAirLineByIATAandICAO(self, iata, icao):
        # Возвращает строку авиакомпании по ее кодам IATA и ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_AL_odbc.execute(SQLQuery)
            if iata is None:
                SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA IS NULL AND AirLineCodeICAO = '" + str(icao) + "' "
            elif icao is None:
                SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA = '" + str(iata) + "' AND AirLineCodeICAO IS NULL "
            elif iata is None and icao is None:
                SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA IS NULL AND AirLineCodeICAO IS NULL "
            else:
                SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA = '" + str(iata) + "' AND AirLineCodeICAO = '" + str(icao) + "' "
            self.seek_AL_odbc.execute(SQLQuery)
            ResultSQL = self.seek_AL_odbc.fetchone()
            self.cnxn_AL_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_AL_odbc.rollback()
        return ResultSQL

    def InsertAirLineByIATAandICAO(self, iata, icao):
        # Вставляем авиакомпанию с кодами IATA и ICAO, альянсом по умолчанию
        # fixme Потом подправить Альанс авиакомпании
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            self.seek_AL_odbc.execute(SQLQuery)
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
            self.seek_AL_odbc.execute(SQLQuery)  # записываем данные по самолету в БД
            ResultSQL = True
            self.cnxn_AL_odbc.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
        except Exception:
            ResultSQL = False
            self.cnxn_AL_odbc.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
        return ResultSQL

    def UpdateAirLineByIATAandICAO(self, id, name, alias, iata, icao, callsign, city, country, status, date, description, aliance):
        # Обновляет данные авиакомпании в один запрос - БЫСТРЕЕ, НАДЕЖНЕЕ
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
            self.seek_AL_odbc.execute(SQLQuery)
            SQLQuery = "UPDATE dbo.AirLinesTable SET AirLine_ID = " + str(id) + ", AirLineName = '" + str(name) + "', AirLineAlias = '" + str(alias)
            SQLQuery += "', AirLineCallSighn = '" + str(callsign)
            SQLQuery += "', AirLineCity = '" + str(city) + "', AirLineCountry = '" + str(country) + "', AirLineStatus = " + str(status)
            SQLQuery += ", CreationDate = '" + str(date) + "', AirLineDescription = '" + str(description) + "', Alliance = " + str(aliance)
            if iata is None:
                print(" ICAO=", str(icao))
                SQLQuery += " WHERE AirLineCodeIATA IS NULL AND AirLineCodeICAO = '" + str(icao) + "' "
            elif icao is None:
                print(" IATA=", str(iata))
                SQLQuery += " WHERE AirLineCodeIATA = '" + str(iata) + "' AND AirLineCodeICAO IS NULL "
            elif iata is None and icao is None:
                print(" IATA=", str(iata), " ICAO=", str(icao))
                SQLQuery += " WHERE AirLineCodeIATA IS NULL AND AirLineCodeICAO IS NULL "
            else:
                print(" IATA=", str(iata), " ICAO=", str(icao))
                SQLQuery += " WHERE AirLineCodeIATA = '" + str(iata) + "' AND AirLineCodeICAO = '" + str(icao) + "' "
            self.seek_AL_odbc.execute(SQLQuery)
            ResultSQL = True
            self.cnxn_AL_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_AL_odbc.rollback()
        return ResultSQL

    class AirCraft:
        def __init__(self):
            pass

    def connectDB_AC_odbc(self, servername, driver, database):
        if self.connectDB_odbc(servername=servername, driver=driver, database=database):
            self.cnxn_AC_odbc = self.cnxn
            self.seek_AC_odbc = self.seek
            return True
        else:
            return False

    def connectDB_AC_mssql(self, servername, database):
        if self.connectDB_mssql(servername=servername, database=database):
            self.cnxn_AC_mssql = self.cnxn
            self.seek_AC_mssql = self.seek
            return True
        else:
            return False

    def connectDSN_AC_odbc(self, dsn):
        if self.connectDSN_odbc(dsn=dsn):
            self.cnxn_AC_odbc = self.cnxn
            self.seek_AC_odbc = self.seek
            return True
        else:
            return False

    def disconnectAC_mssql(self):
        try:
            # Отключаемся от базы данных, курсов закрывается
            self.cnxn_AC_mssql.close()
            print(" -- БД mssql отключена")
        except Exception:
            print(" -- БД mssql уже отключена")

    def disconnectAC_odbc(self):
        try:
            # Закрываем курсор
            self.seek_AC_odbc.close()
            # Отключаемся от базы данных
            self.cnxn_AC_odbc.close()
            print(" -- БД pyodbc отключена")
        except Exception:
            print(" -- БД pyodbc уже отключена")

    def connectDB_ACFN_odbc(self, servername, driver, database):
        if self.connectDB_odbc(servername=servername, driver=driver, database=database):
            self.cnxn_ACFN_odbc = self.cnxn
            self.seek_ACFN_odbc = self.seek
            return True
        else:
            return False

    def connectDSN_ACFN_odbc(self, dsn):
        if self.connectDSN_odbc(dsn=dsn):
            self.cnxn_ACFN_odbc = self.cnxn
            self.seek_ACFN_odbc = self.seek
            return True
        else:
            return False

    def disconnectACFN_odbc(self):
        try:
            # Снимаем курсор
            self.seek_ACFN_odbc.close()
            # Отключаемся от базы данных
            self.cnxn_ACFN_odbc.close()
            print(" -- БД отключена")
        except Exception:
            print(" -- БД уже отключена")

    def QueryAirCraftByRegistration(self, Registration, useAirCrafts):
        # Возвращает строку самолета по его регистрации
        if useAirCrafts:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
                self.seek_AC_odbc.execute(SQLQuery)
                SQLQuery = "SELECT * FROM dbo.AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = '" + str(Registration) + "' "
                self.seek_AC_odbc.execute(SQLQuery)
                ResultSQL = self.seek_AC_odbc.fetchone()  # курсор забирает одну строку и сдвигается на строку вниз
                self.cnxn_AC_odbc.commit()
            except Exception:
                ResultSQL = False
                self.cnxn_AC_odbc.rollback()
        else:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
                self.seek_ACFN_odbc.execute(SQLQuery)
                SQLQuery = "SELECT * FROM dbo.AirCraftsTable WHERE AirCraftRegistration = '" + str(Registration) + "' "
                self.seek_ACFN_odbc.execute(SQLQuery)
                ResultSQL = self.seek_ACFN_odbc.fetchone()  # курсор забирает одну строку и сдвигается на строку вниз
                self.cnxn_ACFN_odbc.commit()
            except Exception:
                ResultSQL = False
                self.cnxn_ACFN_odbc.rollback()
        return ResultSQL

    def InsertAirCraftByRegistration(self, Registration, ALPK, useAirCrafts):
        # Вставляет строку самолета по его регистрации
        if useAirCrafts:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
                self.seek_AC_odbc.execute(SQLQuery)
                SQLQuery = "INSERT INTO dbo.AirCraftsTableNew2XsdIntermediate (AirCraftRegistration) VALUES ('"
                SQLQuery += str(Registration) + "') "
                self.seek_AC_odbc.execute(SQLQuery)  # записываем данные по самолету в БД
                # todo Дописать авиакомпанию-оператора в поле AirFlightsByAirLines -> не надо (он в начале FlightNumberString)
                ResultSQL = True
                self.cnxn_AC_odbc.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
            except Exception:
                ResultSQL = False
                self.cnxn_AC_odbc.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
        else:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
                self.seek_ACFN_odbc.execute(SQLQuery)
                if ALPK is None:
                    SQLQuery = "INSERT INTO dbo.AirCraftsTable (AirCraftRegistration) VALUES ('"
                    SQLQuery += str(Registration) + "') "
                else:
                    SQLQuery = "INSERT INTO dbo.AirCraftsTable (AirCraftRegistration, AirCraftAirLine) VALUES ('"
                    SQLQuery += str(Registration) + "', "
                    SQLQuery += str(ALPK) + ") "
                self.seek_ACFN_odbc.execute(SQLQuery)  # записываем данные по самолету в БД
                ResultSQL = True
                self.cnxn_ACFN_odbc.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
            except Exception:
                ResultSQL = False
                self.cnxn_ACFN_odbc.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
        return ResultSQL

    def UpdateAirCraft(self, Registration, ALPK, useAirCrafts):
        # Обновляет строку самолета с регистрацией (только для табличных данных)
        if useAirCrafts:
            return True
        else:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
                self.seek_ACFN_odbc.execute(SQLQuery)
                SQLQuery = "UPDATE dbo.AirCraftsTable SET AirCraftAirLine = " + str(ALPK) + " WHERE AirCraftRegistration = '" + str(Registration) + "' "
                self.seek_ACFN_odbc.execute(SQLQuery)  # записываем данные по самолету в БД
                ResultSQL = True
                self.cnxn_ACFN_odbc.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
            except Exception:
                ResultSQL = False
                self.cnxn_ACFN_odbc.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
            return ResultSQL

    class AirPort:
        def __init__(self):
            pass

    def connectDB_RT_odbc(self, servername, driver, database):
        if self.connectDB_odbc(servername=servername, driver=driver, database=database):
            self.cnxn_RT_odbc = self.cnxn
            self.seek_RT_odbc = self.seek
            return True
        else:
            return False

    def disconnectRT_odbc(self):
        try:
            # Закрываем курсор
            self.seek_RT_odbc.close()
            # Отключаемся от базы данных
            self.cnxn_RT_odbc.close()
            print(" -- БД отключена")
        except Exception:
            print(" -- БД уже отключена")

    def QueryAirPortByIATA(self, iata):
        # Возвращает строку аэропорта по коду IATA
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeIATA = '" + str(iata) + "' "
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = self.seek_RT_odbc.fetchone()
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def QueryAirPortByICAO(self, icao):
        # Возвращает строку аэропорта по коду ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeICAO = '" + str(icao) + "' "
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = self.seek_RT_odbc.fetchone()
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def QueryAirPortByIATAandICAO(self, iata, icao):
        # Возвращает строку аэропорта по кодам IATA и ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable "
            if iata is None:
                SQLQuery += "WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO = '" + str(icao) + "' "
            elif icao is None:
                SQLQuery += "WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO IS NULL "
            elif iata is None and icao is None:
                SQLQuery += "WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO IS NULL "
            else:
                SQLQuery += "WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO = '" + str(icao) + "' "
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = self.seek_RT_odbc.fetchone()  # выбираем первую строку из возможно нескольких
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def QueryAirPortByFAA_LID(self, faa_lid):
        # Возвращает строку аэропорта по коду ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeFAA_LID = '" + str(faa_lid) + "' "
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = self.seek_RT_odbc.fetchone()
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def QueryAirPortByWMO(self, wmo):
        # Возвращает строку аэропорта по коду ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeWMO = '" + str(wmo) + "' "
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = self.seek_RT_odbc.fetchone()
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def QueryAirRoute(self, IATADeparture, IATAArrival):
        # Возвращает строку маршрута по кодам IATA аэропортов
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = """SELECT dbo.AirRoutesTable.AirRouteUniqueNumber                                 
                       FROM dbo.AirRoutesTable INNER JOIN
                       dbo.AirPortsTable ON dbo.AirRoutesTable.AirPortDeparture = dbo.AirPortsTable.AirPortUniqueNumber INNER JOIN
                       dbo.AirPortsTable AS AirPortsTable_1 ON dbo.AirRoutesTable.AirPortArrival = AirPortsTable_1.AirPortUniqueNumber
                       WHERE (dbo.AirPortsTable.AirPortCodeIATA = '""" + str(IATADeparture) + "') AND (AirPortsTable_1.AirPortCodeIATA = '" + str(IATAArrival) + "') "
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = self.seek_RT_odbc.fetchone()
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def InsertAirPortByIATA(self, iata):
        # fixme дописать функционал, когда код пустой
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "INSERT INTO dbo.AirPortsTable (AirPortCodeIATA) VALUES ('" + str(iata) + "') "
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = True
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def InsertAirPortByIATAandICAO(self, iata, icao):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "INSERT INTO dbo.AirPortsTable (AirPortCodeIATA, AirPortCodeICAO) VALUES ("
            if iata is None:
                SQLQuery += " NULL, '" + str(icao) + "' "
            elif icao is None:
                SQLQuery += " '" + str(iata) + "', NULL "
            elif iata is None and icao is None:
                SQLQuery += " NULL, NULL "
                #print("raise Exception")
                #raise Exception
            else:
                SQLQuery += " '" + str(iata) + "', '" + str(icao) + "' "
            SQLQuery += ") "
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = True
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def InsertAirRoute(self, IATADeparture, IATAArrival):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "INSERT INTO dbo.AirRoutesTable (AirPortDeparture, AirPortArrival) VALUES ("
            SQLQuery += str(IATADeparture) + ", "  # bigint
            SQLQuery += str(IATAArrival) + ") "  # bigint
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = True
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def UpdateAirPortByIATAandICAO(self, csv, hyperlinkWiki, hyperlinkAirPort, hyperlinkOperator, iata, icao, faa_lid, wmo, name, city, county, country, lat, long, height, desc, facilities, incidents):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "UPDATE dbo.AirPortsTable SET SourceCSVFile = '" + str(csv) + "', HyperLinkToWikiPedia = '" + str(hyperlinkWiki) + "', HyperLinkToAirPortSite = '" + str(hyperlinkAirPort) + "', HyperLinkToOperatorSite = '" + str(hyperlinkOperator)
            SQLQuery += "', AirPortCodeFAA_LID = '" + str(faa_lid) + "', AirPortCodeWMO = '" + str(wmo) + "', AirPortName = '" + str(name) + "', AirPortCity = '" + str(city)
            SQLQuery += "', AirPortCounty = '" + str(county) + "', AirPortCountry = '" + str(country) + "', AirPortLatitude = " + str(lat)
            SQLQuery += ", AirPortLongitude = " + str(long) + ", HeightAboveSeaLevel = " + str(height)
            SQLQuery += ", AirPortDescription = '" + str(desc) + "', AirPortFacilities = '" + str(facilities) + "', AirPortIncidents = '" + str(incidents) + "' "
            SQLGeoQuery = ' '
            # todo И надо пересчитать длины маршрутов, завязанных на этот аэропорт
            if lat is not None and long is not None:
                SQLGeoQuery = "UPDATE dbo.AirPortsTable SET AirPortGeo = geography::STPointFromText(CONCAT('POINT(', " + str(long) + ", ' ', " + str(lat) + ", ') '), 4326) "
            else:
                SQLQuery = "UPDATE dbo.AirPortsTable SET AirPortGeo = geography::STPointFromText(CONCAT('POINT(', " + str(0) + ", ' ', " + str(0) + ", ') '), 4326) "
            if iata is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                SQLGeoQuery += Append
            elif icao is None:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                SQLGeoQuery += Append
            elif iata is None and icao is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                SQLGeoQuery += Append
                #print("raise Exception")
                #raise Exception
            else:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                SQLGeoQuery += Append
            self.seek_RT_odbc.execute(SQLQuery)
            self.seek_RT_odbc.execute(SQLGeoQuery)
            ResultSQL = True
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def IncrementLogCountViewedAirPort(self, iata, icao, host, user, dtn):
        try:
            Query = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
            self.seek_RT_odbc.execute(Query)
            SQLQuery = "SELECT LogCountViewed FROM dbo.AirPortsTable"
            XMLQuery = "SELECT LogDateAndTimeViewed FROM dbo.AirPortsTable"
            if iata is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                XMLQuery += Append
            elif icao is None:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                XMLQuery += Append
            elif iata is None and icao is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                XMLQuery += Append
            else:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                XMLQuery += Append
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = self.seek_RT_odbc.fetchone()  # выбираем первую строку из возможно нескольких
            self.seek_RT_odbc.execute(XMLQuery)
            ResultXML = self.seek_RT_odbc.fetchone()
            Count = 1
            #host = 'WorkCompTest1'
            #user = 'ArtemTest20'
            print(" ResultXML = " + str(ResultXML[0]))
            DateTime = ElementTree.Element('DateTime', From=str(host))
            DateTime.text = str(dtn)
            User = ElementTree.Element('User', Name=str(user))
            User.append(DateTime)
            if ResultXML[0] is None:
                root_tag = ElementTree.Element('Viewed')
                root_tag.append(User)
            else:
                Count += ResultSQL[0]
                root_tag = ElementTree.fromstring(ResultXML[0])  # указатель на XML-ную структуру - Element
                Search = root_tag.findall(".//User")
                print(" Search = " + str(Search))
                added = False
                for node in Search:
                    if node.attrib['Name'] == str(user):
                        #newDateTime = ElementTree.SubElement(node, 'DateTime')
                        #newDateTime.attrib['From'] = str(host)
                        #newDateTime.text = str(dtn)
                        #User.append(newDateTime)  # fixme добавляет еще раз
                        # root_tag.insert(3, DateTime)  # вставилась 3-я по счету подветка (не по схеме)
                        node.append(DateTime)
                        #root_tag.append(User)
                        added = True
                        #break
                if not added:
                    #User.append(DateTime)
                    root_tag.append(User)
                xQuery = ".//User[@Name='" + str(user) + "'] "
                print(" xQuery = " + str(xQuery))
            print("LogCountViewed = " + str(Count))
            xml_to_String = ElementTree.tostring(root_tag, method='xml').decode(encoding="utf-8")  # XML-ная строка
            SQLQuery = "UPDATE dbo.AirPortsTable SET LogCountViewed = " + str(Count)
            XMLQuery = "UPDATE dbo.AirPortsTable SET LogDateAndTimeViewed = '" + str(xml_to_String) + "' "
            if iata is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                XMLQuery += Append
            elif icao is None:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                XMLQuery += Append
            elif iata is None and icao is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                XMLQuery += Append
            else:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                XMLQuery += Append
            self.seek_RT_odbc.execute(SQLQuery)
            self.seek_RT_odbc.execute(XMLQuery)
            self.cnxn_RT_odbc.commit()
            Result = True
        except Exception:
            Result = False
            self.cnxn_RT_odbc.rollback()
        return Result

    def IncrementLogCountChangedAirPort(self, iata, icao, host, user, dtn):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "SELECT LogCountChanged FROM dbo.AirPortsTable"
            XMLQuery = "SELECT LogDateAndTimeChanged FROM dbo.AirPortsTable"
            if iata is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                XMLQuery += Append
            elif icao is None:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                XMLQuery += Append
            elif iata is None and icao is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                XMLQuery += Append
            else:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                XMLQuery += Append
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = self.seek_RT_odbc.fetchone()  # выбираем первую строку из возможно нескольких
            self.seek_RT_odbc.execute(XMLQuery)
            ResultXML = self.seek_RT_odbc.fetchone()
            Count = 1
            DateTime = ElementTree.Element('DateTime', From=str(host))
            DateTime.text = str(dtn)
            User = ElementTree.Element('User', Name=str(user))
            User.append(DateTime)
            if ResultXML[0] is None:
                root_tag = ElementTree.Element('Changed')
                root_tag.append(User)
            else:
                Count += ResultSQL[0]
                root_tag = ElementTree.fromstring(ResultXML[0])
                Search = root_tag.findall(".//User")
                added = False
                for node in Search:
                    if node.attrib['Name'] == str(user):
                        node.append(DateTime)
                        added = True
                if not added:
                    root_tag.append(User)
            print("LogCountChanged = " + str(Count))
            xml_to_String = ElementTree.tostring(root_tag, method='xml').decode(encoding="utf-8")
            print(" xml_to_String = " + str(xml_to_String))
            SQLQuery = "UPDATE dbo.AirPortsTable SET LogCountChanged = " + str(Count)
            XMLQuery = "UPDATE dbo.AirPortsTable SET LogDateAndTimeChanged = '" + str(xml_to_String) + "' "
            if iata is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                XMLQuery += Append
            elif icao is None:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                XMLQuery += Append
            elif iata is None and icao is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                XMLQuery += Append
            else:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                XMLQuery += Append
            self.seek_RT_odbc.execute(SQLQuery)
            self.seek_RT_odbc.execute(XMLQuery)
            self.cnxn_RT_odbc.commit()
            Result = True
        except Exception:
            Result = False
            self.cnxn_RT_odbc.rollback()
        return Result

    def ModifyAirFlight(self, ac, al, fn, dep, arr, flightdate, begindate, useAirCrafts, useXQuery, useMSsql, useMarkers):

        class Results:
            def __init__(self):
                self.Result = 0  # Коды возврата: 0 - несработка, 1 - вставили, 2 - сплюсовали

            def getResult(self):
                return self.Result

            def Fail(self):
                self.Result = 0

            def Added(self):
                self.Result = 1

            def Padded(self):
                self.Result = 2

        db_air_route = self.QueryAirRoute(dep, arr).AirRouteUniqueNumber
        Result = 0
        if db_air_route is not None:
            db_air_craft = self.QueryAirCraftByRegistration(ac, useAirCrafts).AirCraftUniqueNumber
            if db_air_craft is not None:
                if useAirCrafts:
                    if useXQuery:
                        try:
                            parameters = (str(ac), str(al) + str(fn), db_air_route, str(flightdate), str(begindate))
                            print("\n parameters = " + str(parameters))
                            if useMSsql:
                                self.seek_AC_mssql.callproc('SPUpdateFlightsByRoutes', parameters=parameters)
                                Data = self.seek_AC_mssql.fetchall()  # fetchval() - pyodbc convenience method similar to cursor.fetchone()[0]
                                self.cnxn_AC_mssql.commit()
                            else:
                                # fixme см. статью https://stackoverflow.com/questions/28635671/using-sql-server-stored-procedures-from-python-pyodbc
                                if useMarkers:
                                    SQLQuery = "CALL SPUpdateFlightsByRoutes ?, ?, ?, ?, ? "
                                    print(" SQLQuery = " + str(SQLQuery))
                                    self.seek_AC_odbc.execute(SQLQuery, parameters)  # fixme 42000 Incorrect syntax near '@P1'
                                    #self.seek_AC_odbc.execute(SQLQuery, str(ac), str(al) + str(fn), str(db_air_route), str(flightdate), str(begindate))  # fixme 42000 Incorrect syntax near '@P1'
                                else:
                                    #SQLQuery = "CALL SPUpdateFlightsByRoutes '" + str(ac) + "', '" + str(al) + str(fn) + "', " + str(db_air_route) + ", '" + str(flightdate) + "', '" + str(begindate) + "' "
                                    SQLQuery = "EXECUTE SPUpdateFlightsByRoutes '" + str(ac) + "', '" + str(al) + str(fn) + "', " + str(db_air_route) + ", '" + str(flightdate) + "', '" + str(begindate) + "' "  # fixme 4200 Incorrect syntax near 'N906DL'
                                    print(" SQLQuery = " + str(SQLQuery))
                                    self.seek_AC_odbc.execute(SQLQuery)  # fixme Incorrect syntax near 'N357UA'
                                Data = self.seek_AC_odbc.fetchall()  # fetchval() - pyodbc convenience method similar to cursor.fetchone()[0]
                                self.cnxn_AC_odbc.commit()
                            if Data:
                                print(" Результат хранимой процедуры = " + str(Data))
                                Result = 1
                            else:
                                Result = 0
                        except Exception as exception:
                            print(" exception = " + str(exception))
                            if useMSsql:
                                self.cnxn_AC_mssql.rollback()
                            else:
                                self.cnxn_AC_odbc.rollback()
                            Result = 0
                    else:
                        # fixme при полной модели восстановления БД на первых 5-ти загрузках файл журнала стал в 1000 раз больше файла данных -> сделал простую
                        try:
                            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
                            self.seek_AC_odbc.execute(SQLQuery)
                            XMLQuery = "SELECT FlightsByRoutes FROM dbo.AirCraftsTableNew2XsdIntermediate WITH (UPDLOCK) WHERE AirCraftRegistration = '" + str(ac) + "' "
                            self.seek_AC_odbc.execute(XMLQuery)
                            ResultXML = self.seek_AC_odbc.fetchone()
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
                                                        Result = 2
                                                if not paddedStep:
                                                    step.text = str(QuantityCounted)
                                                    nodeRoute.append(step)
                                                    addedStep = True
                                                    Result = 1
                                        if not paddedStep and not addedStep:
                                            step.text = str(QuantityCounted)
                                            Route.append(step)
                                            nodeFlight.append(Route)
                                            addedRoute = True
                                            Result = 1
                                if not paddedStep and not addedStep and not addedRoute:
                                    step.text = str(QuantityCounted)
                                    Route.append(step)
                                    Flight.append(Route)
                                    root_tag_FlightsByRoutes.append(Flight)
                                    addedFlight = True
                                    Result = 1
                            xml_FlightsByRoutes_to_String = ElementTree.tostring(root_tag_FlightsByRoutes, method='xml').decode(encoding="utf-8")  # XML-ная строка
                            XMLQuery = "UPDATE dbo.AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes = '" + str(xml_FlightsByRoutes_to_String) + "' WHERE AirCraftRegistration = '" + str(ac) + "' "
                            self.seek_AC_odbc.execute(XMLQuery)
                            self.cnxn_AC_odbc.commit()
                        except Exception:
                            self.cnxn_AC_odbc.rollback()
                            Result = 0
                else:
                    try:
                        SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
                        self.seek_ACFN_odbc.execute(SQLQuery)
                        SQLQuery = "SELECT * FROM dbo.AirFlightsTable WITH (UPDLOCK) WHERE FlightNumberString = '" + str(al) + str(fn) + "' AND AirRoute = "
                        SQLQuery += str(db_air_route) + " AND AirCraft = " + str(db_air_craft) + " AND FlightDate = '" + str(flightdate) + "' AND BeginDate = '" + str(begindate) + "' "
                        self.seek_ACFN_odbc.execute(SQLQuery)
                        ResultQuery = self.seek_ACFN_odbc.fetchone()
                        if ResultQuery is None:
                            SQLQuery = "INSERT INTO dbo.AirFlightsTable (AirRoute, AirCraft, FlightNumberString, QuantityCounted, FlightDate, BeginDate) VALUES ("
                            SQLQuery += str(db_air_route) + ", "  # bigint
                            SQLQuery += str(db_air_craft) + ", '"  # bigint
                            SQLQuery += str(al) + str(fn) + "', "  # nvarchar(50)
                            SQLQuery += str(1) + ", '" + str(flightdate) + "', '" + str(begindate) + "') "  # bigint
                            Result = 1
                        elif ResultQuery is not None:
                            quantity = ResultQuery.QuantityCounted + 1
                            SQLQuery = "UPDATE dbo.AirFlightsTable SET QuantityCounted = " + str(quantity)
                            SQLQuery += " WHERE FlightNumberString = '" + str(al) + str(fn) + "' AND AirRoute = " + str(db_air_route)
                            SQLQuery += " AND AirCraft = " + str(db_air_craft) + " AND FlightDate = '" + str(flightdate) + "' AND BeginDate = '" + str(begindate) + "' "
                            Result = 2
                        else:
                            pass
                        self.seek_ACFN_odbc.execute(SQLQuery)
                        self.cnxn_ACFN_odbc.commit()
                    except Exception:
                        self.cnxn_ACFN_odbc.rollback()
                        Result = 0
                    finally:
                        pass
            elif db_air_craft is None:
                Result = 0
            else:
                Result = 0
        elif db_air_route is None:
            Result = 0
        else:
            Result = 0
        return Result

    def checkConnection(self):
        if self.cnxn_AL_odbc and (self.cnxn_AC_odbc or self.cnxn_ACFN_odbc) and self.cnxn_RT_odbc:
            return True
        else:
            return False