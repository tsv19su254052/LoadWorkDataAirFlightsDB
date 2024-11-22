DECLARE @begindate DATE, @enddate DATE, @currentdate DATE
-- Даем диапазон дат для копирования
SET @begindate = '2012-01-01'
SET @enddate = '2012-12-31'

-- Проверяем
-- сколько было
SET Transaction Isolation Level Read Committed
SELECT COUNT(*) AS LinesCountFromAirFlights
	FROM AirFlightsDBNew72WorkBase.dbo.AirFlightsTable
		WHERE FlightDate BETWEEN @begindate AND @enddate  -- Загружает tempdb
-- и сколько вставилось
SELECT COUNT(*) AS LinesCountFromAirCrafts
	FROM AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByFlightDate
		WHERE FlightDate >= @begindate AND FlightDate <= @enddate  -- Загружает tempdb
-- Сделал индекс на AirFlightsDBNew72WorkBase.dbo.AirFlightsTable.FlightDate -> в 3 раза быстрее
