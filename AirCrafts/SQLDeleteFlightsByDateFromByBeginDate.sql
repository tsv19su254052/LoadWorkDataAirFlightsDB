-- :CONNECT data-server-1.movistar.vrn.skylink.local
-- :CONNECT terminalserver\mssqlserver15
USE AirCraftsDBNew62
GO

DECLARE @faildate DATE
SET @faildate = '2024-04-01'  -- 

-- Смотрим указанный месяц
SET Transaction Isolation Level Read Committed
SELECT AirRoute, AirCraftRegistration, FlightNumberString, QuantityCounted, FlightDate, BeginDate, LoadDate 
  FROM	AirFlightsTableIntermediateByBeginDate 
		INNER JOIN AirCraftsTableNew2XsdIntermediate ON AirFlightsTableIntermediateByBeginDate.AirCraft = AirCraftsTableNew2XsdIntermediate.AirCraftUniqueNumber
	WHERE BeginDate = @faildate
		ORDER BY FlightDate, AirCraftRegistration, FlightNumberString

-- Количество строк за указанный месяц
SELECT COUNT(*) AS LINESCOUNT
  FROM AirFlightsTableIntermediateByBeginDate
	WHERE BeginDate = @faildate

-- Удаляем этот месяц
SET Transaction Isolation Level Serializable
DELETE FROM AirFlightsTableIntermediateByBeginDate WHERE BeginDate = @faildate  -- Загружает tempdb

-- Еще раз смотрим указанный месяц
SET Transaction Isolation Level Read Committed
SELECT AirRoute, AirCraftRegistration, FlightNumberString, QuantityCounted, FlightDate, BeginDate, LoadDate 
  FROM	AirFlightsTableIntermediateByBeginDate 
		INNER JOIN AirCraftsTableNew2XsdIntermediate ON AirFlightsTableIntermediateByBeginDate.AirCraft = AirCraftsTableNew2XsdIntermediate.AirCraftUniqueNumber
	WHERE BeginDate = @faildate
		ORDER BY FlightDate, AirCraftRegistration, FlightNumberString
