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
        self.ServerNameOriginal = "localhost"  # указал имя NetBIOS и указал инстанс
        self.ServerHost = ".\mssqlserver15"
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
        self.useAirFlightsDB = True
        self.useAirCraftsDSN = False
        self.useXQuery = False
        self.SetInputDate = False
        self.BeginDate = ' '


class States:
    def __init__(self):
        # Состояния
        self.Connected_AL = False
        self.Connected_RT = False
        self.Connected_ACFN = False
        self.Connected_AC_XML = False


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
        self.cnxnAL = None  # подключение
        self.seekAL = None  # курсор

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
        self.cnxnAC_mssql = None
        self.cnxnAC_XML = None
        self.cnxnACFN = None
        # Курсоры
        self.seekAC_mssql = None
        self.seekAC_XML = None
        self.seekACFN = None

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
        self.cnxnRT = None  # подключение
        self.seekRT = None  # курсор
        self.LogCountViewed = 0
        self.LogCountChanged = 0

    class AirLine:
        def __init__(self):
            pass

    def connectDB_AL(self, driver, servername, database):
        if self.connectDB(driver=driver, servername=servername, database=database):
            self.cnxnAL = self.cnxn
            self.seekAL = self.seek
            return True
        else:
            return False

    def disconnectAL(self):
        try:
            # Снимаем курсор
            self.seekAL.close()
            # Отключаемся от базы данных
            self.cnxnAL.close()
            print(" -- БД отключена")
        except Exception:
            print(" -- БД уже отключена")
        #self.disconnect()

    def QueryAlliances(self):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAL.execute(SQLQuery)
            SQLQuery = "SELECT AllianceUniqueNumber, AllianceName FROM dbo.AlliancesTable"  # Убрал  ORDER BY AlianceName
            self.seekAL.execute(SQLQuery)
            ResultSQL = self.seekAL.fetchall()
            self.cnxnAL.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAL.rollback()
        return ResultSQL

    def QueryAlliancePKByName(self, name):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAL.execute(SQLQuery)
            SQLQuery = "SELECT AllianceUniqueNumber FROM dbo.AlliancesTable WHERE AllianceName='" + str(name) + "' "  # Убрал  ORDER BY AlianceName
            self.seekAL.execute(SQLQuery)
            ResultSQL = self.seekAL.fetchone()
            self.cnxnAL.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAL.rollback()
        return ResultSQL[0]

    def QueryAirLineByPK(self, pk):
        # Возвращает строку авиакомпании по первичному ключу
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAL.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineUniqueNumber = '" + str(pk) + "' "
            self.seekAL.execute(SQLQuery)
            ResultSQL = self.seekAL.fetchone()
            self.cnxnAL.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAL.rollback()
        return ResultSQL

    def QueryAirLineByIATA(self, iata):
        # Возвращает строку авиакомпании по ее коду IATA
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAL.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA = '" + str(iata) + "' "
            self.seekAL.execute(SQLQuery)
            ResultSQL = self.seekAL.fetchone()
            self.cnxnAL.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAL.rollback()
        return ResultSQL

    def QueryAirLineByICAO(self, icao):
        # Возвращает строку авиакомпании по ее коду ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAL.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeICAO = '" + str(icao) + "' "
            self.seekAL.execute(SQLQuery)
            ResultSQL = self.seekAL.fetchone()
            self.cnxnAL.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAL.rollback()
        return ResultSQL

    def QueryAirLineByIATAandICAO(self, iata, icao):
        # Возвращает строку авиакомпании по ее кодам IATA и ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAL.execute(SQLQuery)
            if iata is None:
                SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA IS NULL AND AirLineCodeICAO = '" + str(icao) + "' "
            elif icao is None:
                SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA = '" + str(iata) + "' AND AirLineCodeICAO IS NULL "
            elif iata is None and icao is None:
                SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA IS NULL AND AirLineCodeICAO IS NULL "
            else:
                SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA = '" + str(iata) + "' AND AirLineCodeICAO = '" + str(icao) + "' "
            self.seekAL.execute(SQLQuery)
            ResultSQL = self.seekAL.fetchone()
            self.cnxnAL.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAL.rollback()
        return ResultSQL

    def InsertAirLineByIATAandICAO(self, iata, icao):
        # Вставляем авиакомпанию с кодами IATA и ICAO, альянсом по умолчанию
        # fixme Потом подправить Альанс авиакомпании
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            self.seekAL.execute(SQLQuery)
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
            self.seekAL.execute(SQLQuery)  # записываем данные по самолету в БД
            ResultSQL = True
            self.cnxnAL.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
        except Exception:
            ResultSQL = False
            self.cnxnAL.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
        return ResultSQL

    def UpdateAirLineByIATAandICAO(self, id, name, alias, iata, icao, callsign, city, country, status, date, description, aliance):
        # Обновляет данные авиакомпании в один запрос - БЫСТРЕЕ, НАДЕЖНЕЕ
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
            self.seekAL.execute(SQLQuery)
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
            self.seekAL.execute(SQLQuery)
            ResultSQL = True
            self.cnxnAL.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAL.rollback()
        return ResultSQL

    class AirCraft:
        def __init__(self):
            pass

    def connectDB_AC_mssql(self, servername, database):
        if self.connectDBmssql(servername=servername, database=database):
            self.cnxnAC_mssql = self.cnxn
            self.seekAC_mssql = self.seek
            return True
        else:
            return False

    def connectDSN_AC_XML(self, dsn):
        if self.connectDSN(dsn=dsn):
            self.cnxnAC_XML = self.cnxn
            self.seekAC_XML = self.seek
            return True
        else:
            return False

    def disconnectAC_mssql(self):
        try:
            # Снимаем курсор
            #self.seekAC_mssql.close()
            # Отключаемся от базы данных
            self.cnxnAC_mssql.close()
            print(" -- БД mssql отключена")
        except Exception:
            print(" -- БД mssql уже отключена")

    def disconnectAC_XML(self):
        try:
            # Снимаем курсор
            self.seekAC_XML.close()
            # Отключаемся от базы данных
            self.cnxnAC_XML.close()
            print(" -- БД pyodbc отключена")
        except Exception:
            print(" -- БД pyodbc уже отключена")
        #self.disconnect()

    def connectDB_ACFN(self, driver, servername, database):
        if self.connectDB(driver=driver, servername=servername, database=database):
            self.cnxnACFN = self.cnxn
            self.seekACFN = self.seek
            return True
        else:
            return False

    def connectDSN_ACFN(self, dsn):
        if self.connectDSN(dsn=dsn):
            self.cnxnACFN = self.cnxn
            self.seekACFN = self.seek
            return True
        else:
            return False

    def disconnectACFN(self):
        try:
            # Снимаем курсор
            self.seekACFN.close()
            # Отключаемся от базы данных
            self.cnxnACFN.close()
            print(" -- БД отключена")
        except Exception:
            print(" -- БД уже отключена")
        #self.disconnect()

    def QueryAirCraftByRegistration(self, Registration, useAirCrafts):
        # Возвращает строку самолета по его регистрации
        if useAirCrafts:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
                self.seekAC_XML.execute(SQLQuery)
                SQLQuery = "SELECT * FROM dbo.AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = '" + str(Registration) + "' "
                self.seekAC_XML.execute(SQLQuery)
                ResultSQL = self.seekAC_XML.fetchone()  # курсор забирает одну строку и сдвигается на строку вниз
                self.cnxnAC_XML.commit()
            except Exception:
                ResultSQL = False
                self.cnxnAC_XML.rollback()
        else:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
                self.seekACFN.execute(SQLQuery)
                SQLQuery = "SELECT * FROM dbo.AirCraftsTable WHERE AirCraftRegistration = '" + str(Registration) + "' "
                self.seekACFN.execute(SQLQuery)
                ResultSQL = self.seekACFN.fetchone()  # курсор забирает одну строку и сдвигается на строку вниз
                self.cnxnACFN.commit()
            except Exception:
                ResultSQL = False
                self.cnxnACFN.rollback()
        return ResultSQL

    def InsertAirCraftByRegistration(self, Registration, ALPK, useAirCrafts):
        # Вставляет строку самолета по его регистрации
        if useAirCrafts:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
                self.seekAC_XML.execute(SQLQuery)
                SQLQuery = "INSERT INTO dbo.AirCraftsTableNew2XsdIntermediate (AirCraftRegistration) VALUES ('"
                SQLQuery += str(Registration) + "') "
                self.seekAC_XML.execute(SQLQuery)  # записываем данные по самолету в БД
                # todo Дописать авиакомпанию-оператора в поле AirFlightsByAirLines -> не надо (он в начале FlightNumberString)
                ResultSQL = True
                self.cnxnAC_XML.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
            except Exception:
                ResultSQL = False
                self.cnxnAC_XML.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
        else:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
                self.seekACFN.execute(SQLQuery)
                if ALPK is None:
                    SQLQuery = "INSERT INTO dbo.AirCraftsTable (AirCraftRegistration) VALUES ('"
                    SQLQuery += str(Registration) + "') "
                else:
                    SQLQuery = "INSERT INTO dbo.AirCraftsTable (AirCraftRegistration, AirCraftAirLine) VALUES ('"
                    SQLQuery += str(Registration) + "', "
                    SQLQuery += str(ALPK) + ") "
                self.seekACFN.execute(SQLQuery)  # записываем данные по самолету в БД
                ResultSQL = True
                self.cnxnACFN.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
            except Exception:
                ResultSQL = False
                self.cnxnACFN.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
        return ResultSQL

    def UpdateAirCraft(self, Registration, ALPK, useAirCrafts):
        # Обновляет строку самолета с регистрацией (только для табличных данных)
        if useAirCrafts:
            return True
        else:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
                self.seekACFN.execute(SQLQuery)
                SQLQuery = "UPDATE dbo.AirCraftsTable SET AirCraftAirLine = " + str(ALPK) + " WHERE AirCraftRegistration = '" + str(Registration) + "' "
                self.seekACFN.execute(SQLQuery)  # записываем данные по самолету в БД
                ResultSQL = True
                self.cnxnACFN.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
            except Exception:
                ResultSQL = False
                self.cnxnACFN.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
            return ResultSQL

    class AirPort:
        def __init__(self):
            pass

    def connectDB_RT(self, driver, servername, database):
        if self.connectDB(driver=driver, servername=servername, database=database):
            self.cnxnRT = self.cnxn
            self.seekRT = self.seek
            return True
        else:
            return False

    def disconnectRT(self):
        try:
            # Снимаем курсор
            self.seekRT.close()
            # Отключаемся от базы данных
            self.cnxnRT.close()
            print(" -- БД отключена")
        except Exception:
            print(" -- БД уже отключена")
        #self.disconnect()

    def QueryAirPortByIATA(self, iata):
        # Возвращает строку аэропорта по коду IATA
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekRT.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeIATA = '" + str(iata) + "' "
            self.seekRT.execute(SQLQuery)
            ResultSQL = self.seekRT.fetchone()
            self.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            self.cnxnRT.rollback()
        return ResultSQL

    def QueryAirPortByICAO(self, icao):
        # Возвращает строку аэропорта по коду ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekRT.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeICAO = '" + str(icao) + "' "
            self.seekRT.execute(SQLQuery)
            ResultSQL = self.seekRT.fetchone()
            self.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            self.cnxnRT.rollback()
        return ResultSQL

    def QueryAirPortByIATAandICAO(self, iata, icao):
        # Возвращает строку аэропорта по кодам IATA и ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekRT.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable "
            if iata is None:
                SQLQuery += "WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO = '" + str(icao) + "' "
            elif icao is None:
                SQLQuery += "WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO IS NULL "
            elif iata is None and icao is None:
                SQLQuery += "WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO IS NULL "
            else:
                SQLQuery += "WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO = '" + str(icao) + "' "
            self.seekRT.execute(SQLQuery)
            ResultSQL = self.seekRT.fetchone()  # выбираем первую строку из возможно нескольких
            self.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            self.cnxnRT.rollback()
        return ResultSQL

    def QueryAirPortByFAA_LID(self, faa_lid):
        # Возвращает строку аэропорта по коду ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekRT.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeFAA_LID = '" + str(faa_lid) + "' "
            self.seekRT.execute(SQLQuery)
            ResultSQL = self.seekRT.fetchone()
            self.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            self.cnxnRT.rollback()
        return ResultSQL

    def QueryAirPortByWMO(self, wmo):
        # Возвращает строку аэропорта по коду ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekRT.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeWMO = '" + str(wmo) + "' "
            self.seekRT.execute(SQLQuery)
            ResultSQL = self.seekRT.fetchone()
            self.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            self.cnxnRT.rollback()
        return ResultSQL

    def QueryAirRoute(self, IATADeparture, IATAArrival):
        # Возвращает строку маршрута по кодам IATA аэропортов
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekRT.execute(SQLQuery)
            SQLQuery = """SELECT dbo.AirRoutesTable.AirRouteUniqueNumber                                 
                       FROM dbo.AirRoutesTable INNER JOIN
                       dbo.AirPortsTable ON dbo.AirRoutesTable.AirPortDeparture = dbo.AirPortsTable.AirPortUniqueNumber INNER JOIN
                       dbo.AirPortsTable AS AirPortsTable_1 ON dbo.AirRoutesTable.AirPortArrival = AirPortsTable_1.AirPortUniqueNumber
                       WHERE (dbo.AirPortsTable.AirPortCodeIATA = '""" + str(IATADeparture) + "') AND (AirPortsTable_1.AirPortCodeIATA = '" + str(IATAArrival) + "') "
            self.seekRT.execute(SQLQuery)
            ResultSQL = self.seekRT.fetchone()
            self.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            self.cnxnRT.rollback()
        return ResultSQL

    def InsertAirPortByIATA(self, iata):
        # fixme дописать функционал, когда код пустой
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            self.seekRT.execute(SQLQuery)
            SQLQuery = "INSERT INTO dbo.AirPortsTable (AirPortCodeIATA) VALUES ('" + str(iata) + "') "
            self.seekRT.execute(SQLQuery)
            ResultSQL = True
            self.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            self.cnxnRT.rollback()
        return ResultSQL

    def InsertAirPortByIATAandICAO(self, iata, icao):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            self.seekRT.execute(SQLQuery)
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
            self.seekRT.execute(SQLQuery)
            ResultSQL = True
            self.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            self.cnxnRT.rollback()
        return ResultSQL

    def InsertAirRoute(self, IATADeparture, IATAArrival):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            self.seekRT.execute(SQLQuery)
            SQLQuery = "INSERT INTO dbo.AirRoutesTable (AirPortDeparture, AirPortArrival) VALUES ("
            SQLQuery += str(IATADeparture) + ", "  # bigint
            SQLQuery += str(IATAArrival) + ") "  # bigint
            self.seekRT.execute(SQLQuery)
            ResultSQL = True
            self.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            self.cnxnRT.rollback()
        return ResultSQL

    def UpdateAirPortByIATAandICAO(self, csv, hyperlinkWiki, hyperlinkAirPort, hyperlinkOperator, iata, icao, faa_lid, wmo, name, city, county, country, lat, long, height, desc, facilities, incidents):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
            self.seekRT.execute(SQLQuery)
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
            self.seekRT.execute(SQLQuery)
            self.seekRT.execute(SQLGeoQuery)
            ResultSQL = True
            self.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            self.cnxnRT.rollback()
        return ResultSQL

    def IncrementLogCountViewedAirPort(self, iata, icao, host, user, dtn):
        try:
            Query = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
            self.seekRT.execute(Query)
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
            self.seekRT.execute(SQLQuery)
            ResultSQL = self.seekRT.fetchone()  # выбираем первую строку из возможно нескольких
            self.seekRT.execute(XMLQuery)
            ResultXML = self.seekRT.fetchone()
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
            self.seekRT.execute(SQLQuery)
            self.seekRT.execute(XMLQuery)
            self.cnxnRT.commit()
            Result = True
        except Exception:
            Result = False
            self.cnxnRT.rollback()
        return Result

    def IncrementLogCountChangedAirPort(self, iata, icao, host, user, dtn):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
            self.seekRT.execute(SQLQuery)
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
            self.seekRT.execute(SQLQuery)
            ResultSQL = self.seekRT.fetchone()  # выбираем первую строку из возможно нескольких
            self.seekRT.execute(XMLQuery)
            ResultXML = self.seekRT.fetchone()
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
            self.seekRT.execute(SQLQuery)
            self.seekRT.execute(XMLQuery)
            self.cnxnRT.commit()
            Result = True
        except Exception:
            Result = False
            self.cnxnRT.rollback()
        return Result

    def ModifyAirFlight(self, ac, al, fn, dep, arr, flightdate, begindate, useAirCrafts, useXQuery):

        class Results:
            def __init__(self):
                self.Result = 0  # Коды возврата: 0 - несработка, 1 - вставили, 2 - сплюсовали

            def Fail(self):
                self.Result = 0

            def Added(self):
                self.Result = 1

            def Padded(self):
                self.Result = 2

        db_air_route = self.QueryAirRoute(dep, arr).AirRouteUniqueNumber
        if db_air_route is not None:
            db_air_craft = self.QueryAirCraftByRegistration(ac, useAirCrafts).AirCraftUniqueNumber
            if db_air_craft is not None:
                if useAirCrafts:
                    if useXQuery:
                        try:
                            #SQLQuery = "DECLARE @ReturnData INT "
                            #SQLQuery += "SET @ReturnData = 5 "
                            #self.seekAC_XML.execute(SQLQuery)
                            # todo При отладке вставлять тестовый файлик. После отладки убрать из БД все тестовые строки и убрать из строки ниже "Test" ...
                            #SQLQuery += "EXECUTE @ReturnData = dbo.SPUpdateFlightsByRoutes '" + str(ac) + "', '" + str(al) + str(fn) + "', " + str(db_air_route) + ", '" + str(flightdate) + "', '" + str(begindate) + "' "
                            #SQLQuery += "SELECT @ReturnData "
                            #print(str(SQLQuery))
                            #self.seekAC_mssql.execute(SQLQuery)
                            #self.seekAC_mssql.execute(SQLQuery)
                            self.seekAC_mssql.callproc('dbo.SPUpdateFlightsByRoutes', (ac, al + fn, db_air_route, flightdate, begindate))  # для библиотеки pymssql (пока не ставится)
                            #Status = self.seekAC_mssql.proc_status
                            #print(" Status = " + str(Status))
                            Data = self.seekAC_mssql.fetchall()  # fetchval() - pyodbc convenience method similar to cursor.fetchone()[0]
                            self.cnxnAC_mssql.commit()
                            if Data:
                                print(" Результат хранимой процедуры = " + str(Data))
                            Result = Data[0][0]
                        except Exception as exception:
                            print(" exception = " + str(exception))
                            self.cnxnAC_mssql.rollback()
                            Result = 0
                    else:
                        # fixme при полной модели восстановления БД на первых 5-ти загрузках файл журнала стал в 1000 раз больше файла данных -> сделал простую
                        try:
                            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
                            self.seekAC_XML.execute(SQLQuery)
                            XMLQuery = "SELECT FlightsByRoutes FROM dbo.AirCraftsTableNew2XsdIntermediate WITH (UPDLOCK) WHERE AirCraftRegistration = '" + str(ac) + "' "
                            self.seekAC_XML.execute(XMLQuery)
                            ResultXML = self.seekAC_XML.fetchone()
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
                            self.seekAC_XML.execute(XMLQuery)
                            self.cnxnAC_XML.commit()
                        except Exception:
                            self.cnxnAC_XML.rollback()
                            Result = 0
                else:
                    try:
                        SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
                        self.seekACFN.execute(SQLQuery)
                        SQLQuery = "SELECT * FROM dbo.AirFlightsTable WITH (UPDLOCK) WHERE FlightNumberString = '" + str(al) + str(fn) + "' AND AirRoute = "
                        SQLQuery += str(db_air_route) + " AND AirCraft = " + str(db_air_craft) + " AND FlightDate = '" + str(flightdate) + "' AND BeginDate = '" + str(begindate) + "' "
                        self.seekACFN.execute(SQLQuery)
                        ResultQuery = self.seekACFN.fetchone()
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
                        self.seekACFN.execute(SQLQuery)
                        self.cnxnACFN.commit()
                    except Exception:
                        self.cnxnACFN.rollback()
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
