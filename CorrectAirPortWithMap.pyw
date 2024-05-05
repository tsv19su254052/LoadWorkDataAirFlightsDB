#  Interpreter 3.7 -> 3.10


import datetime
import sys, io, os, socket, json
from xml.etree import ElementTree
import pyodbc
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets  # pip install PyQtWebEngine -> поставил
import folium
from folium.plugins.draw import Draw
#from PyQt5.QtWebEngineWidgets import QWebEngineView  # pip install PyQtWebEngine -> поставил

# Импорт пользовательской библиотеки (файла *.py в этой же папке)
from FilesWithClasses.Classes import Ui_DialogCorrectAirPortsWithMap, Ui_DialogInputIATAandICAO, AirPort, ServerNames, FileNames, Flags, States


# Делаем экземпляры
class AirPortWork(AirPort):
    def __int__(self):
        pass

    LogCountViewed = 0
    LogCountChanged = 0

S = ServerNames()
F = FileNames()
Fl = Flags()
St = States()


# Основная функция
def myApplication():
    # Одно прикладное приложение
    # todo Делаем сопряжение экземпляров классов с SQL-ными базами данных - семантическими противоположностями ООП, примеров мало
    # fixme Сделать скрипт, который копирует данные таблицы по коду IATA строку за строкой из одной базы в другую
    myApp = QtWidgets.QApplication(sys.argv)
    # Делаем экземпляры
    # fixme Правильно сделать экземпляр с композицией
    myDialog = Ui_DialogCorrectAirPortsWithMap()
    myDialog.setupUi(Dialog=myDialog)  # надо вызывать явно
    myDialog.setFixedSize(920, 780)
    myDialog.setWindowTitle('АэроПорты')
    myDialogInputIATAandICAO = Ui_DialogInputIATAandICAO()
    myDialogInputIATAandICAO.setupUi(Dialog=myDialogInputIATAandICAO)
    myDialogInputIATAandICAO.setFixedSize(240, 245)
    # Дополняем функционал экземпляра главного диалога
    # Переводим в исходное состояние
    myDialog.pushButton_ConnectDB.setToolTip("После подключения нажмите кнопку Поиск")
    myDialog.pushButton_UpdateDB.setToolTip("Запись внесенных изменений в БД \n Перед нажатием правильно заполнить и проверить введенные данные")
    myDialog.pushButton_UpdateDB.setEnabled(False)
    myDialog.pushButton_DisconnectDB.setToolTip("Перед закрытием диалога отключиться от базы данных")
    myDialog.pushButton_DisconnectDB.setEnabled(False)
    # Параметры соединения с сервером
    myDialog.lineEdit_Server.setEnabled(False)
    myDialog.lineEdit_Driver.setEnabled(False)
    myDialog.lineEdit_ODBCversion.setEnabled(False)
    myDialog.lineEdit_DSN.setEnabled(False)
    myDialog.lineEdit_Schema.setEnabled(False)
    # Добавляем базы данных в выпадающий список
    myDialog.comboBox_DB.addItem("AirPortsAndRoutesDBNew62")
    # Получаем список драйверов баз данных
    # Добавляем атрибут DriversODBC по ходу действия
    S.DriversODBC = pyodbc.drivers()
    if S.DriversODBC:
        for DriverODBC in S.DriversODBC:
            if not DriverODBC:
                break
            myDialog.comboBox_Driver.addItem(str(DriverODBC))
    myDialog.textEdit_SourceCSVFile.setEnabled(False)
    myDialog.label_hyperlink_to_WikiPedia.setEnabled(False)
    myDialog.label_HyperLink_to_AirPort.setEnabled(False)
    myDialog.label_HyperLink_to_Operator.setEnabled(False)
    myDialog.textBrowser_HyperLinks.setToolTip("Пока в разработке")
    myDialog.pushButton_HyperLinkChange_Wikipedia.setEnabled(False)
    myDialog.pushButton_HyperLinkChange_AirPort.setEnabled(False)
    myDialog.pushButton_HyperLinkChange_Operator.setEnabled(False)
    myDialog.lineEdit_AirPortCodeFAA_LID.setEnabled(False)
    myDialog.lineEdit_AirPortCodeWMO.setEnabled(False)
    myDialog.pushButton_SearchByIATA.setToolTip("Поиск по коду IATA\n (выводит первую запись из БД, дубликаты не предусматриваются)")
    myDialog.pushButton_SearchByIATA.setEnabled(False)
    myDialog.pushButton_SearchByICAO.setToolTip("Поиск по коду ICAO\n (выводит первую запись из БД, дубликаты не предусматриваются)")
    myDialog.pushButton_SearchByICAO.setEnabled(False)
    myDialog.pushButton_SearchByFAALID.setToolTip("Поиск по коду FAA LID\n (выводит первую запись из БД, дубликаты не предусматриваются)")
    myDialog.pushButton_SearchByFAALID.setEnabled(False)
    myDialog.pushButton_SearchByWMO.setToolTip("Поиск по коду WMO\n (выводит первую запись из БД, дубликаты не предусматриваются)")
    myDialog.pushButton_SearchByWMO.setEnabled(False)
    myDialog.pushButton_SearchAndInsertByIATAandICAO.setToolTip("Считаем, что аэропорт или аэродром однозначно определяются сочетанием кодов IATA и ICAO\nКоды FAA LID (легкомоторная авиация) и WMO дописываются дополнительно\nЕсли код IATA пустой, то вероятно просто аэродром или взлетная полоса без инфраструктуры")
    myDialog.pushButton_SearchAndInsertByIATAandICAO.setEnabled(False)
    myDialog.textEdit_AirPortName.setEnabled(False)
    myDialog.textEdit_AirPortCity.setEnabled(False)
    myDialog.textEdit_AirPortCounty.setEnabled(False)
    myDialog.textEdit_AirPortCountry.setEnabled(False)
    myDialog.lineEdit_AirPortLatitude.setEnabled(False)
    myDialog.lineEdit_AirPortLongitude.setEnabled(False)
    myDialog.lineEdit_HeightAboveSeaLevel.setEnabled(False)
    myDialog.textBrowser_HyperLinks.setOpenExternalLinks(True)
    myDialog.textBrowser_HyperLinks.setReadOnly(True)
    myDialog.textBrowser_HyperLinks.setEnabled(False)
    myDialog.pushButton_HyperLinksChange.setToolTip("Изменение адресов ссылок")
    myDialog.pushButton_HyperLinksChange.setEnabled(False)
    myDialog.tabWidget.setTabText(0, "Описание")
    myDialog.tabWidget.setTabText(1, "Сооружения")
    myDialog.tabWidget.setTabText(2, "Случаи")
    myDialog.tabWidget.setTabText(3, "На карте")
    myDialog.tabWidget.setTabText(4, "Дополнительно")
    myDialog.tab_1.setToolTip("Общее описание аэропорта. История развития")
    myDialog.tab_2.setToolTip("Инфраструктура аэропорта, сооружения, хабы, арендаторы, склады, ангары")
    myDialog.tab_3.setToolTip("Случаи и инциденты")
    myDialog.tab_4.setToolTip("Расположение объекта на карте")
    myDialog.tab_5.setToolTip("Оснащение аппаратурой взаимодействия с самолетами (пока в разработке)")
    myDialog.textEdit_AirPortDescription.setEnabled(False)
    myDialog.textEdit_AirPortFacilities.setEnabled(False)
    myDialog.textEdit_Incidents.setEnabled(False)
    myDialog.verticalLayout_Map.setEnabled(False)
    myDialogInputIATAandICAO.lineEdit_CodeIATA.setToolTip("Введите код IATA или поставьте галочку, если его нет")
    myDialogInputIATAandICAO.lineEdit_CodeICAO.setToolTip("Введите код ICAO или поставьте галочку, если его нет")
    myDialogInputIATAandICAO.checkBox_Status_IATA.setToolTip("Пустая ячейка в БД (не считается, как пустая строка)")
    myDialogInputIATAandICAO.checkBox_Status_ICAO.setToolTip("Пустая ячейка в БД (не считается, как пустая строка)")
    myDialogInputIATAandICAO.pushButton_SearchInsert.setToolTip("Внимательно проверить введенные данные. Исправления после вставки не предусматриваются")
    # Добавляем атрибут ввода
    myDialog.lineEditCodeIATA = QtWidgets.QLineEdit()
    myDialog.lineEditCodeICAO = QtWidgets.QLineEdit()
    myDialog.lineEditCodeFAA_LID = QtWidgets.QLineEdit()
    myDialog.lineEditCodeWMO = QtWidgets.QLineEdit()
    # Привязки обработчиков
    myDialog.pushButton_ConnectDB.clicked.connect(lambda: PushButtonConnectDB())
    myDialog.pushButton_UpdateDB.clicked.connect(lambda: PushButtonUpdateDB())
    myDialog.pushButton_DisconnectDB.clicked.connect(lambda: PushButtonDisconnect())
    myDialog.pushButton_HyperLinkChange_Wikipedia.clicked.connect(lambda: PushButtonChangeHyperLinkWikiPedia())
    myDialog.pushButton_HyperLinkChange_AirPort.clicked.connect(lambda: PushButtonChangeHyperLinkAirPort())
    myDialog.pushButton_HyperLinkChange_Operator.clicked.connect(lambda: PushButtonChangeHyperLinkOperator())
    myDialog.pushButton_SearchByIATA.clicked.connect(lambda: PushButtonSearchByIATA())
    myDialog.pushButton_SearchByICAO.clicked.connect(lambda: PushButtonSearchByICAO())
    myDialog.pushButton_SearchByFAALID.clicked.connect(lambda: PushButtonSearchByFAA_LID())
    myDialog.pushButton_SearchByWMO.clicked.connect(lambda: PushButtonSearchByWMO())
    myDialog.pushButton_SearchAndInsertByIATAandICAO.clicked.connect(lambda: PushButtonInsertByIATAandICAO())
    myDialog.pushButton_HyperLinksChange.clicked.connect(lambda: PushButtonChangeHyperLinks())
    myDialogInputIATAandICAO.pushButton_SearchInsert.clicked.connect(lambda: PushButtonInput())
    myDialogInputIATAandICAO.checkBox_Status_IATA.clicked.connect(lambda: Check_IATA())
    myDialogInputIATAandICAO.checkBox_Status_ICAO.clicked.connect(lambda: Check_ICAO())

    def ClearMap():
        # очищаем предыдущую отрисовку
        if myDialog.verticalLayout_Map is not None:
            while myDialog.verticalLayout_Map.count():
                child = myDialog.verticalLayout_Map.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    myDialog.verticalLayout_Map.clearLayout(child.layout())


    def SwitchingGUI(Key):
        myDialog.comboBox_DB.setEnabled(not Key)
        myDialog.comboBox_Driver.setEnabled(not Key)
        myDialog.lineEdit_Server.setEnabled(Key)
        myDialog.lineEdit_Driver.setEnabled(Key)
        myDialog.lineEdit_ODBCversion.setEnabled(Key)
        myDialog.lineEdit_DSN.setEnabled(Key)
        myDialog.lineEdit_Schema.setEnabled(Key)
        myDialog.textEdit_SourceCSVFile.setEnabled(Key)
        myDialog.label_hyperlink_to_WikiPedia.setEnabled(Key)
        myDialog.label_HyperLink_to_AirPort.setEnabled(Key)
        myDialog.label_HyperLink_to_Operator.setEnabled(Key)
        myDialog.pushButton_HyperLinkChange_Wikipedia.setEnabled(Key)
        myDialog.pushButton_HyperLinkChange_AirPort.setEnabled(Key)
        myDialog.pushButton_HyperLinkChange_Operator.setEnabled(Key)
        myDialog.lineEdit_AirPortCodeFAA_LID.setEnabled(Key)
        myDialog.lineEdit_AirPortCodeWMO.setEnabled(Key)
        myDialog.pushButton_SearchByIATA.setEnabled(Key)
        myDialog.pushButton_SearchByICAO.setEnabled(Key)
        myDialog.pushButton_SearchByFAALID.setEnabled(Key)
        myDialog.pushButton_SearchByWMO.setEnabled(Key)
        myDialog.pushButton_SearchAndInsertByIATAandICAO.setEnabled(Key)
        myDialog.textEdit_AirPortName.setEnabled(Key)
        myDialog.textEdit_AirPortCity.setEnabled(Key)
        myDialog.textEdit_AirPortCounty.setEnabled(Key)
        myDialog.textEdit_AirPortCountry.setEnabled(Key)
        myDialog.lineEdit_AirPortLatitude.setEnabled(Key)
        myDialog.lineEdit_AirPortLongitude.setEnabled(Key)
        myDialog.lineEdit_HeightAboveSeaLevel.setEnabled(Key)
        myDialog.textBrowser_HyperLinks.setEnabled(Key)
        myDialog.pushButton_HyperLinksChange.setEnabled(Key)
        myDialog.textEdit_AirPortDescription.setEnabled(Key)
        myDialog.textEdit_AirPortFacilities.setEnabled(Key)
        myDialog.textEdit_Incidents.setEnabled(Key)
        ClearMap()
        myDialog.verticalLayout_Map.setEnabled(Key)

    def IncrementLogCountViewedAirPort(iata, icao, host, user, dtn):
        try:
            Query = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
            S.seekRT.execute(Query)
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
            S.seekRT.execute(SQLQuery)
            ResultSQL = S.seekRT.fetchone()  # выбираем первую строку из возможно нескольких
            S.seekRT.execute(XMLQuery)
            ResultXML = S.seekRT.fetchone()
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
            S.seekRT.execute(SQLQuery)
            S.seekRT.execute(XMLQuery)
            S.cnxnRT.commit()
            Result = True
        except Exception:
            Result = False
            S.cnxnRT.rollback()
        else:
            pass
        finally:
            return Result

    def ReadingQuery(ResultQuery):
        AirPortWork.SourceCSVFile = ResultQuery.SourceCSVFile
        AirPortWork.HyperLinkToWikiPedia = ResultQuery.HyperLinkToWikiPedia
        AirPortWork.HyperLinkToAirPortSite = ResultQuery.HyperLinkToAirPortSite
        AirPortWork.HyperLinkToOperatorSite = ResultQuery.HyperLinkToOperatorSite
        AirPortWork.AirPortCodeIATA = ResultQuery.AirPortCodeIATA
        AirPortWork.AirPortCodeICAO = ResultQuery.AirPortCodeICAO
        AirPortWork.AirPortCodeFAA_LID = ResultQuery.AirPortCodeFAA_LID
        AirPortWork.AirPortCodeWMO = ResultQuery.AirPortCodeWMO
        AirPortWork.AirPortName = ResultQuery.AirPortName
        AirPortWork.AirPortCity = ResultQuery.AirPortCity
        AirPortWork.AirPortCounty = ResultQuery.AirPortCounty
        AirPortWork.AirPortCountry = ResultQuery.AirPortCountry
        AirPortWork.AirPortLatitude = ResultQuery.AirPortLatitude
        AirPortWork.AirPortLongitude = ResultQuery.AirPortLongitude
        AirPortWork.HeightAboveSeaLevel = ResultQuery.HeightAboveSeaLevel
        AirPortWork.AirPortDescription = ResultQuery.AirPortDescription
        AirPortWork.AirPortFacilities = ResultQuery.AirPortFacilities
        AirPortWork.AirPortIncidents = ResultQuery.AirPortIncidents
        AirPortWork.LogCountViewed = ResultQuery.LogCountViewed
        AirPortWork.LogCountChanged = ResultQuery.LogCountChanged
        IncrementLogCountViewedAirPort(AirPortWork.AirPortCodeIATA, AirPortWork.AirPortCodeICAO, socket.gethostname(), os.getlogin(), datetime.datetime.now())

    @QtCore.pyqtSlot("QWebEngineDownloadItem*")
    def ExportGeoJSON(self, item):
        print(" выбираем путь записи файла *.geojson")
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Записать файл геоданных", ' ', item.suggestedFileName())
        if path:
            print(str(path))
            item.setPath(path)
            item.accept()

    def SetFields():
        # Выводим записи
        myDialog.textEdit_SourceCSVFile.clear()
        myDialog.textEdit_SourceCSVFile.append(str(AirPortWork.SourceCSVFile))
        myDialog.label_hyperlink_to_WikiPedia.setText("<a href=" + str(AirPortWork.HyperLinkToWikiPedia) + ">Wikipedia</a>")
        myDialog.label_hyperlink_to_WikiPedia.setToolTip(str(AirPortWork.HyperLinkToWikiPedia))
        myDialog.label_hyperlink_to_WikiPedia.setOpenExternalLinks(True)
        myDialog.label_HyperLink_to_AirPort.setText("<a href=" + str(AirPortWork.HyperLinkToAirPortSite) + ">Сайт аэропорта или аэродрома</a>")
        myDialog.label_HyperLink_to_AirPort.setToolTip(str(AirPortWork.HyperLinkToAirPortSite))
        myDialog.label_HyperLink_to_AirPort.setOpenExternalLinks(True)
        myDialog.label_HyperLink_to_Operator.setText("<a href=" + str(AirPortWork.HyperLinkToOperatorSite) + ">Сайт оператора аэропорта</a>")
        myDialog.label_HyperLink_to_Operator.setToolTip(str(AirPortWork.HyperLinkToOperatorSite))
        myDialog.label_HyperLink_to_Operator.setOpenExternalLinks(True)
        if AirPortWork.AirPortCodeIATA is None:
            myDialog.label_CodeIATA.setText(" ")
        else:
            myDialog.label_CodeIATA.setText(str(AirPortWork.AirPortCodeIATA))
        if AirPortWork.AirPortCodeICAO is None:
            myDialog.label_CodeICAO.setText(" ")
        else:
            myDialog.label_CodeICAO.setText(AirPortWork.AirPortCodeICAO)
        myDialog.lineEdit_AirPortCodeFAA_LID.setText(str(AirPortWork.AirPortCodeFAA_LID))
        myDialog.lineEdit_AirPortCodeWMO.setText(str(AirPortWork.AirPortCodeWMO))
        myDialog.textEdit_AirPortName.clear()
        myDialog.textEdit_AirPortName.append(str(AirPortWork.AirPortName))
        myDialog.textEdit_AirPortCity.clear()
        myDialog.textEdit_AirPortCity.append(str(AirPortWork.AirPortCity))
        myDialog.textEdit_AirPortCounty.clear()
        myDialog.textEdit_AirPortCounty.append(str(AirPortWork.AirPortCounty))
        myDialog.textEdit_AirPortCountry.clear()
        myDialog.textEdit_AirPortCountry.append(str(AirPortWork.AirPortCountry))
        myDialog.lineEdit_AirPortLatitude.setText(str(AirPortWork.AirPortLatitude))
        myDialog.lineEdit_AirPortLongitude.setText(str(AirPortWork.AirPortLongitude))
        myDialog.lineEdit_HeightAboveSeaLevel.setText(str(AirPortWork.HeightAboveSeaLevel))
        myDialog.textBrowser_HyperLinks.clear()
        #myDialog.textBrowser_HyperLinks.append("<a href=" + str(A.SourceCSVFile) + ">Wikipedia</a>")
        #myDialog.textBrowser_HyperLinks.append("<a href=" + str(A.SourceCSVFile) + ">Сайт аэропорта или аэродрома</a>")
        #myDialog.textBrowser_HyperLinks.append("<a href=" + str(A.SourceCSVFile) + ">Сайт оператора аэропорта</a>")
        myDialog.textEdit_AirPortDescription.clear()
        myDialog.textEdit_AirPortDescription.append(str(AirPortWork.AirPortDescription))
        myDialog.textEdit_AirPortFacilities.clear()
        myDialog.textEdit_AirPortFacilities.append(AirPortWork.AirPortFacilities)
        myDialog.textEdit_Incidents.clear()
        myDialog.textEdit_Incidents.append(AirPortWork.AirPortIncidents)
        ClearMap()
        if AirPortWork.AirPortLatitude is not None and AirPortWork.AirPortLongitude is not None:
            coordinates = (AirPortWork.AirPortLatitude, AirPortWork.AirPortLongitude)
            # Варианты карт:
            #  - OpenStreetMap (подробная цветная),
            #  - CartoDB Positron (серенькая),
            #  - CartoDB Voyager (аскетичная, мало подписей и меток),
            #  - NASAGIBS Blue Marble (пока не отрисовывается),
            #  - Stamen Terrain - не работает,
            #  - Esri - не работает,
            #  - OpenWeatherMap - не работает,
            zoom = 13
            m = folium.Map(tiles=None, zoom_start=zoom, location=coordinates)
            folium.TileLayer("CartoDB Positron").add_to(m)
            folium.TileLayer("CartoDB Voyager").add_to(m)
            folium.TileLayer("NASAGIBS Blue Marble").add_to(m)
            folium.TileLayer("OpenStreetMap").add_to(m)
            folium.raster_layers.TileLayer(tiles='http://mt1.google.com/vt/lyrs=m&h1=p1Z&x={x}&y={y}&z={z}',
                                           name='Google Roadmap',
                                           attr='Google Map', ).add_to(m)
            folium.raster_layers.TileLayer(tiles='http://mt1.google.com/vt/lyrs=s&h1=p1Z&x={x}&y={y}&z={z}',
                                           name='Google Satellite', attr='Google Map', ).add_to(m)
            folium.raster_layers.TileLayer(tiles='http://mt1.google.com/vt/lyrs=y&h1=p1Z&x={x}&y={y}&z={z}',
                                           name='Google Hybrid',
                                           attr='Google Map', ).add_to(m)
            folium.TileLayer(show=True).add_to(m)
            folium.LayerControl().add_to(m)
            m.add_child(folium.LatLngPopup())
            # fixme Export не работает -> см. https://stackoverflow.com/questions/64402959/cant-export-coordinates-on-folium-draw-polygon-in-pyqt5-app
            Draw(export=True,
                 filename="my_data.geojson",
                 position="topleft",
                 draw_options={"polyline": True, "rectangle": True, "circle": True, "circlemarker": True, },
                 edit_options={"poly": {"allowIntersection": False}}, ).add_to(m)
            # save map data to data object
            data = io.BytesIO()
            m.save(data, close_file=False)

            class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
                def javaScriptConsoleMessage(self, level, msg, line, sourceID):
                    coords_dict = json.loads(msg)
                    coords = coords_dict['geometry']['coordinates'][0]
                    print(str(coords))

            webView = QtWebEngineWidgets.QWebEngineView()
            webView.page().profile().downloadRequested.connect(lambda: ExportGeoJSON)  # fixme функция-обработчик не вызывается, connect не работает
            page = WebEnginePage(webView)
            webView.setPage(page)
            webView.setHtml(data.getvalue().decode())
            # новая отрисовка
            myDialog.verticalLayout_Map.addWidget(webView)

    def PushButtonConnectDB():
        if not St.Connected_RT:
            # Переводим в неактивное состояние
            myDialog.pushButton_ConnectDB.setEnabled(False)
            # Подключаемся к базе данных по выбранному источнику
            ChoiceDB = myDialog.comboBox_DB.currentText()
            ChoiceDriver = myDialog.comboBox_Driver.currentText()
            # Добавляем атрибуты DataBase, DriverODBC
            S.DataBase = str(ChoiceDB)
            S.DriverODBC = str(ChoiceDriver)
            try:
                # Добавляем атрибут cnxn
                # через драйвер СУБД + клиентский API-курсор
                S.cnxnRT = pyodbc.connect(driver=S.DriverODBC, server=S.ServerName, database=S.DataBase)
                print("  База данных ", S.DataBase, " подключена")
                # Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде, в СУБД по умолчанию FALSE
                S.cnxnRT.autocommit = False
                print("autocommit is disabled")
                # Ставим набор курсоров
                # КУРСОР нужен для перехода функционального языка формул на процедурный или для вставки процедурных кусков в функциональный скрипт.
                # Способы реализации курсоров:
                #  - SQL, Transact-SQL,
                #  - серверные API-курсоры (OLE DB, ADO, ODBC),
                #  - клиентские API-курсоры (выборка кэшируется на клиенте)
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
                S.seekRT = S.cnxnRT.cursor()
                print("seeks is on")
                St.Connected_RT = True
                # SQL Server
                myDialog.lineEdit_Server.setText(S.cnxnRT.getinfo(pyodbc.SQL_SERVER_NAME))
                # Драйвер
                myDialog.lineEdit_Driver.setText(S.cnxnRT.getinfo(pyodbc.SQL_DRIVER_NAME))
                # версия ODBC
                myDialog.lineEdit_ODBCversion.setText(S.cnxnRT.getinfo(pyodbc.SQL_ODBC_VER))
                # Источник данных
                myDialog.lineEdit_DSN.setText(S.cnxnRT.getinfo(pyodbc.SQL_DATA_SOURCE_NAME))
                # Схема (если из-под другой учетки, то выводит имя учетки)
                # todo Схема по умолчанию - dbo
                myDialog.lineEdit_Schema.setText(S.cnxnRT.getinfo(pyodbc.SQL_USER_NAME))
                # Переводим в рабочее состояние (продолжение)
                SwitchingGUI(True)
                myDialog.pushButton_DisconnectDB.setEnabled(True)
            except Exception:
                # Переводим в рабочее состояние
                myDialog.pushButton_ConnectDB.setEnabled(True)
                message = QtWidgets.QMessageBox()
                message.setText("Нет подключения к базе данных аэропортов")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
            else:
                pass
            finally:
                pass

    def PushButtonDisconnect():
        # кнопка 'Отключиться от базы данных' нажата
        if St.Connected_RT:
            # Переводим в неактивное состояние
            myDialog.pushButton_DisconnectDB.setEnabled(False)
            # Снимаем курсоры
            S.seekRT.close()
            # Отключаемся от базы данных
            S.cnxnRT.close()
            # Снимаем флаги
            St.Connected_RT = False
            # Переводим в рабочее состояние (продолжение)
            SwitchingGUI(False)
            myDialog.pushButton_UpdateDB.setEnabled(False)  # возможно пока не тут
            myDialog.pushButton_ConnectDB.setEnabled(True)

    def UpdateAirPortByIATAandICAO(csv, hyperlinkWiki, hyperlinkAirPort, hyperlinkOperator, iata, icao, faa_lid, wmo, name, city, county, country, lat, long, height, desc, facilities, incidents):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
            S.seekRT.execute(SQLQuery)
            SQLQuery = "UPDATE dbo.AirPortsTable SET SourceCSVFile = '" + str(csv) + "', HyperLinkToWikiPedia = '" + str(hyperlinkWiki) + "', HyperLinkToAirPortSite = '" + str(hyperlinkAirPort) + "', HyperLinkToOperatorSite = '" + str(hyperlinkOperator)
            SQLQuery += "', AirPortCodeFAA_LID = '" + str(faa_lid) + "', AirPortCodeWMO = '" + str(wmo) + "', AirPortName = '" + str(name) + "', AirPortCity = '" + str(city)
            SQLQuery += "', AirPortCounty = '" + str(county) + "', AirPortCountry = '" + str(country) + "', AirPortLatitude = " + str(lat)
            SQLQuery += ", AirPortLongitude = " + str(long) + ", HeightAboveSeaLevel = " + str(height)
            SQLQuery += ", AirPortDescription = '" + str(desc) + "', AirPortFacilities = '" + str(facilities) + "', AirPortIncidents = '" + str(incidents) + "' "
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
            S.seekRT.execute(SQLQuery)
            S.seekRT.execute(SQLGeoQuery)
            ResultSQL = True
            S.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            S.cnxnRT.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def PushButtonUpdateDB():
        AirPortWork.SourceCSVFile = myDialog.textEdit_SourceCSVFile.toPlainText()
        #A.AirPortCodeIATA = myDialog.lineEdit_AirPortCodeIATA.text()
        #A.AirPortCodeICAO = myDialog.lineEdit_AirPortCodeICAO.text()
        AirPortWork.AirPortCodeFAA_LID = myDialog.lineEdit_AirPortCodeFAA_LID.text()
        AirPortWork.AirPortCodeWMO = myDialog.lineEdit_AirPortCodeWMO.text()
        AirPortWork.AirPortName = myDialog.textEdit_AirPortName.toPlainText()
        AirPortWork.AirPortCity = myDialog.textEdit_AirPortCity.toPlainText()
        AirPortWork.AirPortCounty = myDialog.textEdit_AirPortCounty.toPlainText()
        AirPortWork.AirPortCountry = myDialog.textEdit_AirPortCountry.toPlainText()
        AirPortWork.AirPortLatitude = myDialog.lineEdit_AirPortLatitude.text()
        AirPortWork.AirPortLongitude = myDialog.lineEdit_AirPortLongitude.text()
        AirPortWork.HeightAboveSeaLevel = myDialog.lineEdit_HeightAboveSeaLevel.text()
        AirPortWork.AirPortDescription = myDialog.textEdit_AirPortDescription.toPlainText()
        AirPortWork.AirPortFacilities = myDialog.textEdit_AirPortFacilities.toPlainText()
        AirPortWork.AirPortIncidents = myDialog.textEdit_Incidents.toPlainText()
        DBAirPort = QueryAirPortByIATAandICAO(iata=AirPortWork.AirPortCodeIATA, icao=AirPortWork.AirPortCodeICAO)
        LogCountChangedCurrent = DBAirPort.LogCountChanged
        if LogCountChangedCurrent is None or (AirPortWork.LogCountChanged is not None and LogCountChangedCurrent is not None and AirPortWork.LogCountChanged == LogCountChangedCurrent):
            # Вносим изменение
            ResultUpdate = UpdateAirPortByIATAandICAO(AirPortWork.SourceCSVFile,
                                                      AirPortWork.HyperLinkToWikiPedia,
                                                      AirPortWork.HyperLinkToAirPortSite,
                                                      AirPortWork.HyperLinkToOperatorSite,
                                                      AirPortWork.AirPortCodeIATA,
                                                      AirPortWork.AirPortCodeICAO,
                                                      AirPortWork.AirPortCodeFAA_LID,
                                                      AirPortWork.AirPortCodeWMO,
                                                      AirPortWork.AirPortName,
                                                      AirPortWork.AirPortCity,
                                                      AirPortWork.AirPortCounty,
                                                      AirPortWork.AirPortCountry,
                                                      AirPortWork.AirPortLatitude,
                                                      AirPortWork.AirPortLongitude,
                                                      AirPortWork.HeightAboveSeaLevel,
                                                      AirPortWork.AirPortDescription,
                                                      AirPortWork.AirPortFacilities,
                                                      AirPortWork.AirPortIncidents)
            if ResultUpdate:
                # fixme Пользователи без права на изменение не фиксируются
                IncrementLogCountChangedAirPort(AirPortWork.AirPortCodeIATA, AirPortWork.AirPortCodeICAO, socket.gethostname(), os.getlogin(), datetime.datetime.now())
                DBAirPort = QueryAirPortByIATAandICAO(AirPortWork.AirPortCodeIATA, AirPortWork.AirPortCodeICAO)
                AirPortWork.LogCountChanged = DBAirPort.LogCountChanged
            else:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не переписалась")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
        else:
            qm = QtWidgets.QMessageBox()
            qm.setText("Перечитайте данные (уже изменены)")
            qm.setIcon(QtWidgets.QMessageBox.Warning)
            qm.exec_()

    def PushButtonChangeHyperLinkWikiPedia():
        Link, ok = QtWidgets.QInputDialog.getText(myDialog, "Ссылка", "Введите адрес сайта")
        if ok:
            AirPortWork.HyperLinkToWikiPedia = Link
            print(str(Link))
            myDialog.label_hyperlink_to_WikiPedia.setText("<a href=" + str(AirPortWork.HyperLinkToWikiPedia) + ">Wikipedia</a>")
            myDialog.label_hyperlink_to_WikiPedia.setToolTip(str(AirPortWork.HyperLinkToWikiPedia))
            myDialog.label_hyperlink_to_WikiPedia.setOpenExternalLinks(True)

    def PushButtonChangeHyperLinkAirPort():
        Link, ok = QtWidgets.QInputDialog.getText(myDialog, "Ссылка", "Введите адрес сайта")
        if ok:
            AirPortWork.HyperLinkToAirPortSite = Link
            print(str(Link))
            myDialog.label_HyperLink_to_AirPort.setText("<a href=" + str(AirPortWork.HyperLinkToAirPortSite) + ">Сайт аэропорта или аэродрома</a>")
            myDialog.label_HyperLink_to_AirPort.setToolTip(str(AirPortWork.HyperLinkToAirPortSite))
            myDialog.label_HyperLink_to_AirPort.setOpenExternalLinks(True)

    def PushButtonChangeHyperLinkOperator():
        Link, ok = QtWidgets.QInputDialog.getText(myDialog, "Ссылка", "Введите адрес сайта")
        if ok:
            AirPortWork.HyperLinkToOperatorSite = Link
            print(str(Link))
            myDialog.label_HyperLink_to_Operator.setText("<a href=" + str(AirPortWork.HyperLinkToOperatorSite) + ">Сайт оператора аэропорта</a>")
            myDialog.label_HyperLink_to_Operator.setToolTip(str(AirPortWork.HyperLinkToOperatorSite))
            myDialog.label_HyperLink_to_Operator.setOpenExternalLinks(True)

    def PushButtonChangeHyperLinks():
        message = QtWidgets.QMessageBox()
        message.setText("Пока в разработке")
        message.setIcon(QtWidgets.QMessageBox.Information)
        message.exec_()

    def QueryAirPortByIATA(iata):
        # Возвращает строку аэропорта по коду IATA
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            S.seekRT.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeIATA = '" + str(iata) + "' "
            S.seekRT.execute(SQLQuery)
            ResultSQL = S.seekRT.fetchone()
            S.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            S.cnxnRT.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def PushButtonSearchByIATA():
        # Кнопка "Поиск" нажата
        Code, ok = QtWidgets.QInputDialog.getText(myDialog, "Код IATA", "Введите код IATA")
        if ok:
            DBAirPort = QueryAirPortByIATA(Code)
            # fixme Решение 3 - не перезаписывать код IATA (Недостаток - можно сделать дубликат по коду ICAO, их много, возможно это НОРМА, исправлять только вручную)
            # fixme Решение 4 - код IATA всегда неактивный, он вводится только при вставке
            if DBAirPort is None:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не найдена")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
            else:
                ReadingQuery(DBAirPort)
                SetFields()
                myDialog.pushButton_UpdateDB.setEnabled(True)

    def QueryAirPortByICAO(icao):
        # Возвращает строку аэропорта по коду ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            S.seekRT.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeICAO = '" + str(icao) + "' "
            S.seekRT.execute(SQLQuery)
            ResultSQL = S.seekRT.fetchone()
            S.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            S.cnxnRT.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def PushButtonSearchByICAO():
        # Кнопка "Поиск" нажата
        Code, ok = QtWidgets.QInputDialog.getText(myDialog, "Код ICAO", "Введите код ICAO")
        if ok:
            DBAirPort = QueryAirPortByICAO(Code)
            if DBAirPort is None:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не найдена")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
            else:
                ReadingQuery(DBAirPort)
                SetFields()
                myDialog.pushButton_UpdateDB.setEnabled(True)

    def QueryAirPortByFAA_LID(faa_lid):
        # Возвращает строку аэропорта по коду ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            S.seekRT.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeFAA_LID = '" + str(faa_lid) + "' "
            S.seekRT.execute(SQLQuery)
            ResultSQL = S.seekRT.fetchone()
            S.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            S.cnxnRT.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def PushButtonSearchByFAA_LID():
        # Кнопка "Поиск" нажата
        Code, ok = QtWidgets.QInputDialog.getText(myDialog, "Код FAA LID", "Введите код FAA LID")
        if ok:
            DBAirPort = QueryAirPortByFAA_LID(Code)
            if DBAirPort is None:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не найдена")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
            else:
                ReadingQuery(DBAirPort)
                SetFields()
                myDialog.pushButton_UpdateDB.setEnabled(True)

    def QueryAirPortByWMO(wmo):
        # Возвращает строку аэропорта по коду ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            S.seekRT.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeWMO = '" + str(wmo) + "' "
            S.seekRT.execute(SQLQuery)
            ResultSQL = S.seekRT.fetchone()
            S.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            S.cnxnRT.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def PushButtonSearchByWMO():
        # Кнопка "Поиск" нажата
        Code, ok = QtWidgets.QInputDialog.getText(myDialog, "Код WMO", "Введите код WMO")
        if ok:
            DBAirPort = QueryAirPortByWMO(Code)
            if DBAirPort is None:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не найдена")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
            else:
                ReadingQuery(DBAirPort)
                SetFields()
                myDialog.pushButton_UpdateDB.setEnabled(True)

    def Check_IATA():
        if myDialogInputIATAandICAO.checkBox_Status_IATA.isChecked():
            myDialogInputIATAandICAO.lineEdit_CodeIATA.setEnabled(False)
        else:
            myDialogInputIATAandICAO.lineEdit_CodeIATA.setEnabled(True)

    def Check_ICAO():
        if myDialogInputIATAandICAO.checkBox_Status_ICAO.isChecked():
            myDialogInputIATAandICAO.lineEdit_CodeICAO.setEnabled(False)
        else:
            myDialogInputIATAandICAO.lineEdit_CodeICAO.setEnabled(True)

    def InsertAirPortByIATAandICAO(iata, icao):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            S.seekRT.execute(SQLQuery)
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
            S.seekRT.execute(SQLQuery)
            ResultSQL = True
            S.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            S.cnxnRT.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def QueryAirPortByIATAandICAO(iata, icao):
        # Возвращает строку аэропорта по кодам IATA и ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            S.seekRT.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable "
            if iata is None:
                SQLQuery += "WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO = '" + str(icao) + "' "
            elif icao is None:
                SQLQuery += "WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO IS NULL "
            elif iata is None and icao is None:
                SQLQuery += "WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO IS NULL "
            else:
                SQLQuery += "WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO = '" + str(icao) + "' "
            S.seekRT.execute(SQLQuery)
            ResultSQL = S.seekRT.fetchone()  # выбираем первую строку из возможно нескольких
            S.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            S.cnxnRT.rollback()
        else:
            pass
        finally:
            return ResultSQL


    def IncrementLogCountChangedAirPort(iata, icao, host, user, dtn):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
            S.seekRT.execute(SQLQuery)
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
            S.seekRT.execute(SQLQuery)
            ResultSQL = S.seekRT.fetchone()  # выбираем первую строку из возможно нескольких
            S.seekRT.execute(XMLQuery)
            ResultXML = S.seekRT.fetchone()
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
            S.seekRT.execute(SQLQuery)
            S.seekRT.execute(XMLQuery)
            S.cnxnRT.commit()
            Result = True
        except Exception:
            Result = False
            S.cnxnRT.rollback()
        else:
            pass
        finally:
            return Result

    def PushButtonInput():
        if myDialogInputIATAandICAO.checkBox_Status_IATA.isChecked():
            Code_IATA = None
        else:
            Code_IATA = myDialogInputIATAandICAO.lineEdit_CodeIATA.text()
        if myDialogInputIATAandICAO.checkBox_Status_ICAO.isChecked():
            Code_ICAO = None
        else:
            Code_ICAO = myDialogInputIATAandICAO.lineEdit_CodeICAO.text()
        DBAirPort = QueryAirPortByIATAandICAO(iata=Code_IATA, icao=Code_ICAO)
        myDialogInputIATAandICAO.close()

        if DBAirPort is None:
            # Вставляем новую запись fixme вставилась запись с Code_IATA = NULL и Code_ICAO = "None"
            ResultInsert = InsertAirPortByIATAandICAO(Code_IATA, Code_ICAO)
            if ResultInsert:
                DBAirPort = QueryAirPortByIATAandICAO(Code_IATA, Code_ICAO)
                if DBAirPort is None:
                    message = QtWidgets.QMessageBox()
                    message.setText("Запись не прочиталась. Попробуйте прочитать ее через поиск")
                    message.setIcon(QtWidgets.QMessageBox.Warning)
                    message.exec_()
                else:
                    ReadingQuery(DBAirPort)
                    SetFields()
                    # fixme Пользователи без права на изменение не фиксируются
                    IncrementLogCountChangedAirPort(Code_IATA, Code_ICAO, socket.gethostname(), os.getlogin(), datetime.datetime.now())
                    DBAirPort = QueryAirPortByIATAandICAO(AirPortWork.AirPortCodeIATA, AirPortWork.AirPortCodeICAO)
                    AirPortWork.LogCountChanged = DBAirPort.LogCountChanged
            else:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не вставилась")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
        else:
            # Переходим на найденную запись
            ReadingQuery(DBAirPort)
            SetFields()
            message = QtWidgets.QMessageBox()
            message.setText("Такая запись есть")
            message.setIcon(QtWidgets.QMessageBox.Information)
            message.exec_()

    def PushButtonInsertByIATAandICAO():
        # кнопка "Поиск и Вставка"
        # Отрисовка диалога ввода
        myDialogInputIATAandICAO.setWindowTitle("Диалог ввода")
        myDialogInputIATAandICAO.setWindowModality(QtCore.Qt.ApplicationModal)
        myDialogInputIATAandICAO.show()

    # Отрисовка первого окна
    myDialog.show()
    # Правильное закрытие окна
    sys.exit(myApp.exec_())


# Точка входа
# __name__ — это специальная переменная, которая будет равна __main__, только если файл запускается как основная программа,
# в остальных случаях - имени модуля при импорте в качестве модуля
if __name__ == "__main__":
    myApplication()
