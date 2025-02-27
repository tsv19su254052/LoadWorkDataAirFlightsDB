-- :CONNECT data-server-1.movistar.vrn.skylink.local
-- :CONNECT terminalserver\mssqlserver15
USE AirFlightsDBNew72WorkBase
GO

DECLARE @faildate DATE
SET @faildate = '2004-04-01'  -- 

-- смотрим указанный месяц
SET Transaction Isolation Level Read Committed
SELECT AirRoute, AirCraftRegistration, FlightNumberString, QuantityCounted, FlightDate, BeginDate, LoadDate 
  FROM	AirFlightsTable 
		INNER JOIN AirCraftsTable ON AirFlightsTable.AirCraft = AirCraftsTable.AirCraftUniqueNumber
	WHERE BeginDate = @faildate
		ORDER BY FlightDate, AirCraftRegistration, FlightNumberString

-- количество строк за указанный месяц
SELECT COUNT(*) AS LINESCOUNT
  FROM AirFlightsTable
  WHERE BeginDate = @faildate

-- удаляем этот месяц
SET Transaction Isolation Level Serializable
-- DELETE FROM AirFlightsTable WHERE BeginDate = @faildate

-- еще раз смотрим указанный месяц
SET Transaction Isolation Level Read Committed
SELECT AirRoute, AirCraftRegistration, FlightNumberString, QuantityCounted, FlightDate, BeginDate, LoadDate 
  FROM AirFlightsTable INNER JOIN AirCraftsTable ON AirFlightsTable.AirCraft = AirCraftsTable.AirCraftUniqueNumber
	WHERE BeginDate = @faildate
		ORDER BY FlightDate, AirCraftRegistration, FlightNumberString
