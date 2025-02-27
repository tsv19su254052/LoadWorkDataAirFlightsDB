-- :CONNECT data-server-1.movistar.vrn.skylink.local
-- :CONNECT terminalserver\mssqlserver15
USE AirCraftsDBNew62
GO

DECLARE @begindate DATE, @enddate DATE
-- Даем диапазон дат для копирования
SET @begindate = '2024-01-01'
SET @enddate = '2024-12-31'

-- Смотрим указанный месяц
SET Transaction Isolation Level Read Committed
SELECT AirRoute, AirCraftRegistration, FlightNumberString, QuantityCounted, FlightDate, BeginDate, LoadDate 
  FROM	AirFlightsTableIntermediateByFlightDate
		INNER JOIN AirCraftsTableNew2XsdIntermediate ON AirFlightsTableIntermediateByFlightDate.AirCraft = AirCraftsTableNew2XsdIntermediate.AirCraftUniqueNumber
	WHERE FlightDate BETWEEN @begindate AND @enddate
		ORDER BY FlightDate, AirCraftRegistration, FlightNumberString

-- Количество строк за указанный месяц
SELECT COUNT(*) AS LINESCOUNT
  FROM AirFlightsTableIntermediateByFlightDate
	WHERE FlightDate BETWEEN @begindate AND @enddate

SET Transaction Isolation Level Serializable
-- Удаляем за этот диапазон дат
DELETE FROM AirFlightsTableIntermediateByFlightDate 
	WHERE FlightDate BETWEEN @begindate AND @enddate  -- Загружает tempdb
-- Удаляем все
-- DELETE FROM AirFlightsTableIntermediateByFlightDate

-- Еще раз смотрим указанный месяц
SET Transaction Isolation Level Read Committed
SELECT AirRoute, AirCraftRegistration, FlightNumberString, QuantityCounted, FlightDate, BeginDate, LoadDate 
  FROM	AirFlightsTableIntermediateByFlightDate 
		INNER JOIN AirCraftsTableNew2XsdIntermediate ON AirFlightsTableIntermediateByFlightDate.AirCraft = AirCraftsTableNew2XsdIntermediate.AirCraftUniqueNumber
	WHERE FlightDate BETWEEN @begindate AND @enddate
		ORDER BY FlightDate, AirCraftRegistration, FlightNumberString
