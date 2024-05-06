#  Interpreter 3.7 -> 3.10
from PyQt5 import QtWidgets, QtCore, QtGui  # оставил 5-ую версию, потому что много наработок еще завязаны на нее
from xml.etree import ElementTree
# todo ветка библиотек Qt - QtCore, QtGui, QtNetwork, QtOpenGL, QtScript, QtSQL (медленнее чем pyodbc), QtDesigner, QtXml
# Руководство по установке см. https://packaging.python.org/tutorials/installing-packages/

# Пользовательская библиотека с классами
from moduleClassServerExchange import ServerExchange
# Задача создания пользовательских структур данных не расматривается -> Только функционал
# Компилируется и кладется в папку __pycache__
# Идея выноса каждого класса в этот отдельный файл, как на Java -> Удобство просмотра типов данных, не особо практично


class ServerNames:
    # Имена серверов
    #ServerNameOriginal = "data-server-1.movistar.vrn.skylink.local"
    ServerNameOriginal = "localhost\mssqlserver15"  # указал имя NetBIOS и указал инстанс
    #ServerNameOriginal = "localhost\sqldeveloper"  # указал инстанс
    # fixme Забыл отменить обратно, надо проверить как самолеты и авиарейсы грузились без него причем в рабочую базу -> Все нормально, этот выбор работал, если грузить не через системный DSN
    ServerNameFlights = "data-server-1.movistar.vrn.skylink.local"  # указал ресурсную запись из DNS
    ServerName = "localhost\mssqlserver15"  # указал инстанс
    #ServerName = "localhost\sqldeveloper"  # указал инстанс


class FileNames:
    # Имена читаемых и записываемых файлов
    InputFileCSV = ' '
    LogFileTXT = ' '
    ErrorFileTXT = 'LogReport_Errors.txt'


class Flags:
    # Флаги
    useAirFlightsDB = True
    useAirCraftsDSN = False
    useXQuery = False
    SetInputDate = False
    BeginDate = ' '


class States:
    # Состояния
    Connected_AL = False
    Connected_RT = False
    Connected_ACFN = False
    Connected_AC_XML = False


SE = ServerExchange()


# fixme правильно писать конструктор
# todo Объявления внутри класса с конструктором и без
class AirLine(SE):
    def __init__(self):
        self.AirLine_ID = 1
        self.AirLineName = " "
        self.AirLineAlias = " "
        self.AirLineCodeIATA = " "
        self.AirLineCodeICAO = " "
        self.AirLineCallSighn = " "
        self.AirLineCity = " "
        self.AirLineCountry = " "
        self.AirLineStatus = 1
        self.CreationDate = '1920-01-01'
        self.AirLineDescription = " "
        self.Alliance = 4
        self.Position = 1  # Позиция курсора в таблице (в SQL начинается с 1)
        self.cnxnAL = None  # подключение
        self.seekAL = None  # курсор

    def connectDB_AL(self, driver, servername, database):
        connection = SE.connectDB(driver=driver, servername=servername, database=database)
        if connection[0]:
            self.cnxnAL = connection[1]
            self.seekAL = connection[2]
            return True
        else:
            return False

    def connectDSN_AL(self, dsn):
        connection = SE.connectDSN(dsn=dsn)
        if connection[0]:
            self.cnxnAL = connection[1]
            self.seekAL = connection[2]
            return True
        else:
            return False

    def disconnectAL(self):
        # Снимаем курсор
        self.seekAL.close()
        # Отключаемся от базы данных
        self.cnxnAL.close()

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


class AirCraft(ServerExchange):
    def __init__(self):
        self.AirCraftModel = 387  # Unknown Model
        self.BuildDate = '1990-01-01'
        self.RetireDate = '1990-01-01'
        self.SourceCSVFile = " "
        self.AirCraftDescription = " "
        self.AirCraftLineNumber_LN = " "
        self.AirCraftLineNumber_MSN = " "
        self.AirCraftSerialNumber_SN = " "
        self.AirCraftCNumber = " "
        self.EndDate = '1990-01-01'
        self.Position = 1  # Позиция курсора в таблице (в SQL начинается с 1)
        # Подключения
        self.cnxnAC_XML = None
        self.cnxnAC = None
        self.cnxnFN = None
        # Курсоры
        self.seekAC_XML = None
        self.seekAC = None
        self.seekFN = None

    def connectDB_AC(self, driver, servername, database):
        connection = SE.connectDB(driver=driver, servername=servername, database=database)
        if connection[0]:
            self.cnxnAC = connection[1]
            self.seekAC = connection[2]
            return True
        else:
            return False

    def connectDSN_AC(self, dsn):
        connection = SE.connectDSN(dsn=dsn)
        if connection[0]:
            self.cnxnAC = connection[1]
            self.seekAC = connection[2]
            return True
        else:
            return False

    def connectDB_FN(self, driver, servername, database):
        connection = SE.connectDB(driver=driver, servername=servername, database=database)
        if connection[0]:
            self.cnxnFN = connection[1]
            self.seekFN = connection[2]
            return True
        else:
            return False

    def connectDSN_FN(self, dsn):
        connection = SE.connectDSN(dsn=dsn)
        if connection[0]:
            self.cnxnFN = connection[1]
            self.seekFN = connection[2]
            return True
        else:
            return False

    def disconnectAC(self):
        # Снимаем курсор
        self.seekAC.close()
        # Отключаемся от базы данных
        self.cnxnAC.close()

    def disconnectFN(self):
        # Снимаем курсор
        self.seekFN.close()
        # Отключаемся от базы данных
        self.cnxnFN.close()

    def disconnectAC_XML(self):
        # Снимаем курсор
        self.seekAC_XML.close()
        # Отключаемся от базы данных
        self.cnxnAC_XML.close()

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
                self.seekAC.execute(SQLQuery)
                SQLQuery = "SELECT * FROM dbo.AirCraftsTable WHERE AirCraftRegistration = '" + str(Registration) + "' "
                self.seekAC.execute(SQLQuery)
                ResultSQL = self.seekAC.fetchone()  # курсор забирает одну строку и сдвигается на строку вниз
                self.cnxnAC.commit()
            except Exception:
                ResultSQL = False
                self.cnxnAC.rollback()
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
                self.seekAC.execute(SQLQuery)
                if ALPK is None:
                    SQLQuery = "INSERT INTO dbo.AirCraftsTable (AirCraftRegistration) VALUES ('"
                    SQLQuery += str(Registration) + "') "
                else:
                    SQLQuery = "INSERT INTO dbo.AirCraftsTable (AirCraftRegistration, AirCraftAirLine) VALUES ('"
                    SQLQuery += str(Registration) + "', "
                    SQLQuery += str(ALPK) + ") "
                self.seekAC.execute(SQLQuery)  # записываем данные по самолету в БД
                ResultSQL = True
                self.cnxnAC.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
            except Exception:
                ResultSQL = False
                self.cnxnAC.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
        return ResultSQL

    def UpdateAirCraft(self, Registration, ALPK, useAirCrafts):
        # Обновляет строку самолета с регистрацией (только для табличных данных)
        if useAirCrafts:
            return True
        else:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
                self.seekAC.execute(SQLQuery)
                SQLQuery = "UPDATE dbo.AirCraftsTable SET AirCraftAirLine = " + str(ALPK) + " WHERE AirCraftRegistration = '" + str(Registration) + "' "
                self.seekAC.execute(SQLQuery)  # записываем данные по самолету в БД
                ResultSQL = True
                self.cnxnAC.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
            except Exception:
                ResultSQL = False
                self.cnxnAC.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
            return ResultSQL


class AirPort(ServerExchange):
    def __init__(self):
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

    def connectDB_RT(self, driver, servername, database):
        connection = SE.connectDB(driver=driver, servername=servername, database=database)
        if connection[0]:
            self.cnxnAL = connection[1]
            self.seekAL = connection[2]
            return True
        else:
            return False

    def connectDSN_RT(self, dsn):
        connection = SE.connectDSN(dsn=dsn)
        if connection[0]:
            self.cnxnAL = connection[1]
            self.seekAL = connection[2]
            return True
        else:
            return False

    def disconnectRT(self):
        # Снимаем курсор
        self.seekRT.close()
        # Отключаемся от базы данных
        self.cnxnRT.close()

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

