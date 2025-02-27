-- Тут собираем вьюшку по авиаперелетам с регистрациями и с аэропортами 
DECLARE @RemoteServer NVARCHAR(500)
SET @RemoteServer = 'data-server-1.movistar.vrn.skylink.local'

BEGIN TRY  -- На результат не влияет
	exec sp_addlinkedserver @server = @RemoteServer  -- срабатывает один раз, но иногда не с первого раза (лучше вынести в отдельный запрос) и работает на сеанс работы в SSMS, на следующие разы выдает ошибку
	PRINT ' Внешний сервер = ' + @RemoteServer + ' привязан'
END TRY
BEGIN CATCH
	PRINT ' Внешний сервер = ' + @RemoteServer + ' не привязался (уже привязан)'
END CATCH

exec sp_linkedservers

DECLARE @City VARCHAR(250), @Reg VARCHAR(50)
SET @Reg = 'N288WN'  -- регистрация самолета
SET @City = 'Denver'  -- аэропорт (аэродром)
SET STATISTICS XML ON

-- :CONNECT terminalserver\mssqlserver15  -- тогда отваливается база на внешнем сервере
-- :CONNECT data-server-1.movistar.vrn.skylink.local  -- Становимся только на внешний сервер -> Но не видит базы на этом сервере
-- USE AirFlightsDBNew62WorkBase  -- Используем эту базу
DROP TABLE IF EXISTS #AirFlightsCraftsTempTable

SET Transaction Isolation Level Read Committed
SELECT  AirCraftsTable.AirCraftUniqueNumber,
		AirFlightsTable.AirCraft,
		AirFlightsTable.AirFlightUniqueNumber,
		AirCraftsTable.AirCraftRegistration,
		AirFlightsTable.FlightDate,
		AirFlightsTable.FlightNumberString,
		AirFlightsTable.QuantityCounted,
		AirCraftsTable.SourceCSVFile,
		AirFlightsTable.AirRoute  
	INTO #AirFlightsCraftsTempTable  -- тут появляются временные таблицы (см. снимок экрана), видна только внутри этого запроса и только для этого запроса (многопользовательский режим)
		FROM    [data-server-1.movistar.vrn.skylink.local].AirFlightsDBNew62WorkBase.dbo.AirFlightsTable INNER JOIN
				[data-server-1.movistar.vrn.skylink.local].AirFlightsDBNew62WorkBase.dbo.AirCraftsTable ON AirFlightsTable.AirCraft = AirCraftsTable.AirCraftUniqueNumber
			WHERE AirCraftRegistration = @Reg

-- DISCONNECT
-- :CONNECT terminalserver\mssqlserver15  -- тогда отваливается база на внешнем сервере
-- USE AirPortsAndRoutesDBNew62  -- выдает ошибку, что этой базы не существует
BEGIN DISTRIBUTED TRANSACTION
	SET Transaction Isolation Level Read Committed
	SELECT		#AirFlightsCraftsTempTable.FlightDate AS FLIGHTDATE,
				#AirFlightsCraftsTempTable.FlightNumberString AS FN,
				#AirFlightsCraftsTempTable.QuantityCounted,
				AirPortsTable.AirPortName AS DEPARTURE,
				AirPortsTable.AirPortCity AS CITY_OUT,
				AirPortsTable.AirPortCodeIATA AS IATA_OUT,
				AirPortsTable_1.AirPortName AS ARRIVAL,
				AirPortsTable_1.AirPortCity AS CITY_IN,
				AirPortsTable_1.AirPortCodeIATA AS IATA_IN,
				#AirFlightsCraftsTempTable.SourceCSVFile AS SOURCEFILE
		FROM	#AirFlightsCraftsTempTable INNER JOIN  -- todo: пересобрать соединения -> Пересобрал, но не видит базу AirPortsAndRoutesDBNew62 ниже
				AirPortsAndRoutesDBNew62.dbo.AirRoutesTable ON #AirFlightsCraftsTempTable.AirRoute = AirRoutesTable.AirRouteUniqueNumber INNER JOIN
				AirPortsAndRoutesDBNew62.dbo.AirPortsTable ON AirRoutesTable.AirPortDeparture = AirPortsTable.AirPortUniqueNumber INNER JOIN
				AirPortsAndRoutesDBNew62.dbo.AirPortsTable AS AirPortsTable_1 ON AirRoutesTable.AirPortArrival = AirPortsTable_1.AirPortUniqueNumber  
			WHERE #AirFlightsCraftsTempTable.AirCraftRegistration = @Reg
			ORDER BY FLIGHTDATE, FN, CITY_OUT, CITY_IN  -- 32292

	SELECT		AirPortsTable.AirPortName AS DEPARTURE,
				AirPortsTable.AirPortCity AS CITY_OUT,
				AirPortsTable.AirPortCodeIATA AS IATA_OUT,
				AirPortsTable_1.AirPortName AS ARRIVAL,
				AirPortsTable_1.AirPortCity AS CITY_IN,
				AirPortsTable_1.AirPortCodeIATA AS IATA_IN,
				SUM(#AirFlightsCraftsTempTable.QuantityCounted) AS QUANTITY
		FROM	#AirFlightsCraftsTempTable INNER JOIN  -- todo: пересобрать соединения -> Пересобрал, но не видит базу AirPortsAndRoutesDBNew62 ниже
				AirPortsAndRoutesDBNew62.dbo.AirRoutesTable ON #AirFlightsCraftsTempTable.AirRoute = AirRoutesTable.AirRouteUniqueNumber INNER JOIN
				AirPortsAndRoutesDBNew62.dbo.AirPortsTable ON AirRoutesTable.AirPortDeparture = AirPortsTable.AirPortUniqueNumber INNER JOIN
				AirPortsAndRoutesDBNew62.dbo.AirPortsTable AS AirPortsTable_1 ON AirRoutesTable.AirPortArrival = AirPortsTable_1.AirPortUniqueNumber  
			WHERE #AirFlightsCraftsTempTable.AirCraftRegistration = @Reg AND (AirPortsTable.AirPortCity = @City OR AirPortsTable_1.AirPortCity = @City)
			GROUP BY	AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortName,
						AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortCity,
						AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortCodeIATA,
						AirPortsTable_1.AirPortName,
						AirPortsTable_1.AirPortCity,
						AirPortsTable_1.AirPortCodeIATA
			ORDER BY CITY_OUT, CITY_IN  -- 166
COMMIT TRANSACTION

-- DISCONNECT

/*
BEGIN TRY
	exec sp_dropserver @server = @RemoteServer
	PRINT ' Внешний сервер = ' + @RemoteServer + ' отвязан'
END TRY
BEGIN CATCH
	PRINT ' Внешний сервер = ' + @RemoteServer + ' не отвязался (уже отвязан)'
END CATCH

exec sp_linkedservers
*/

-- Вывод:
-- большие самолеты American AirLines, Continental как правило летают реже и более привязаны к маршруту
	-- UTair Boeing 767-224(ER):
		-- VP-BAG UTair Aviation 15.07.2012 Moscow - Dushanbe, Tashkent, Makhachkala - Jeddah, Anadyr		(N76156 Continental Airlines 15.02.2001 -> United Airlines 01.12.2011) 95 строк
		-- VP-BAI UTair Aviation 02.09.2012 Moscow - Dushanbe, Tashkent, Bukhara, Anadyr					(N67158 Continental Airlines 30.05.2001 -> United Airlines 01.12.2011) 97 строк
		-- VP-BAL UTair Aviation 21.07.2014 Moscow - Dushanbe, Tashkent, Bukhara							(N68160 Continental Airlines 30.10.2001 -> United Airlines 01.12.2011) 157 строк
	-- New York City 11.09.2001
		-- N334AA - 11.09.2001 New York City 92(i)+1600 crashed into WTC Northern tower 8:45 am after hyjack ER Boston - Los Angeles flight #11, tt 58350, 11538 l, most died at collapse of tower at 10:29 am, own NEMLC 8.07.87, FUNB r6.01.00 118 строк
		-- N612UA - 11.09.2001 New York City 65(i)+1000 crashed into WTC Southern tower 9:03 am after hyjack ER Boston - Los Angeles flight #175, tt 66647, 17549 l, most occ. killed when tower collapsed at 09:50 am 179 строк
