--  опируем перелеты из базы авиаперелетов в таблицу базы самолетов

DECLARE @begindate DATE, @enddate DATE, @currentdate DATE, @rt BIGINT, @ac BIGINT, @reg VARCHAR(50), @acnew BIGINT, @fns VARCHAR(50), @q BIGINT, @fd DATE, @bd DATE, @ReturnValue INT, @fails BIGINT
SET @begindate = '2024-04-01'
SET @enddate = '2024-05-01'
SET @currentdate = @begindate
SET @fails = 0

-- —мотрим вначале
SET Transaction Isolation Level Read Committed
SELECT COUNT(*) AS LinesCountTotal
	FROM AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByBeginDate  -- «агружает tempdb

SET Transaction Isolation Level Serializable
WHILE @currentdate <= @enddate
	--  опируем по одному мес€цу года (врем€ выполнени€ без хранимки - 56 ... 58 мин, с хранимкой - 18 суток)
	BEGIN
		DECLARE cursor_flight CURSOR FORWARD_ONLY STATIC FOR
			SELECT	AirRoute,
					AirCraft,
					FlightNumberString,  -- возможно надо конвертировать Unicode -> cp-1251
					QuantityCounted,
					FlightDate,
					BeginDate
					FROM AirFlightsDBNew72WorkBase.dbo.AirFlightsTable
						WHERE AirFlightsDBNew72WorkBase.dbo.AirFlightsTable.BeginDate = @currentdate
							ORDER BY AirCraft, FlightNumberString
		PRINT ' + курсор объ€влен'

		OPEN cursor_flight  -- заполн€ет указанный выше набор
		FETCH NEXT FROM cursor_flight INTO @rt, @ac, @fns, @q, @fd, @bd  -- становитс€ на первую строку и присваивает ее переменным

		WHILE @@FETCH_STATUS = 0
			BEGIN
				/*
				SET @acnew = (SELECT TOP 1 AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate.AirCraftUniqueNumber
								FROM	AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate
								INNER JOIN AirFlightsDBNew72WorkBase.dbo.AirCraftsTable ON AirCraftsTable.AirCraftRegistration = AirCraftsTableNew2XsdIntermediate.AirCraftRegistration
								INNER JOIN AirFlightsDBNew72WorkBase.dbo.AirFlightsTable ON AirFlightsTable.AirCraft = AirCraftsTable.AirCraftUniqueNumber
									WHERE AirFlightsDBNew72WorkBase.dbo.AirFlightsTable.AirCraft = @ac)
				*/
				SET @acnew = (SELECT AirCraftUniqueNumber 
								FROM AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate 
									WHERE AirCraftRegistration = (SELECT AirCraftRegistration FROM AirFlightsDBNew72WorkBase.dbo.AirCraftsTable 
																	WHERE AirCraftUniqueNumber = @ac))

				INSERT INTO AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByBeginDate(
					AirRoute,  -- BIGINT NOT NULL, сделать индекс
					AirCraft,  -- BIGINT NOT NULL - внешний ключ на регистрацию самолета, сделать индекс
					FlightNumberString,  -- VARCHAR(50) NOT NULL, сделать индекс
					QuantityCounted,  -- BIGINT
					FlightDate,  -- DATE
					BeginDate,  -- DATE
					LoadDate) VALUES (@rt, @acnew, @fns, @q, @fd, @bd, GETDATE())
				/*
				SET @reg = (SELECT AirCraftRegistration FROM AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate WHERE AirCraftUniqueNumber = @acnew)
				EXECUTE @ReturnValue = AirCraftsDBNew62.dbo.SPFlightInsertOrUpdate @reg, @fns, @rt, @fd, @bd  -- есть отказы из-за взаимоблокировок
				IF @ReturnValue = 0
					SET @fails += 1
				*/
				FETCH NEXT FROM cursor_flight
				INTO @rt, @ac, @fns, @q, @fd, @bd
			END
		CLOSE cursor_flight
		DEALLOCATE cursor_flight

		-- PRINT ' + date = ' + CONVERT(VARCHAR(100), @currentdate)
		SELECT	@currentdate AS CurrentMonth,
				COUNT(*) AS LinesCount
			FROM AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByBeginDate
				WHERE BeginDate = @currentdate  -- «агружает tempdb
		SET @currentdate = DATEADD(MONTH, 1, @currentdate)
	END

PRINT ' + перелеты скопированы, отказов = ' +  CONVERT(VARCHAR(100), @fails)

-- ѕровер€ем и сравниваем что и сколько вставилось
/*
SET Transaction Isolation Level Read Committed  -- Ckbirjv vyjuj -> ¬ыдает шибку
SELECT COUNT(*) AS LinesCountAllMonthsBefore
	FROM AirFlightsDBNew72WorkBase.dbo.AirFlightsTable
		WHERE AirFlightsDBNew72WorkBase.dbo.AirFlightsTable.BeginDate >= @begindate AND AirFlightsDBNew72WorkBase.dbo.AirFlightsTable.BeginDate <= @enddate  -- «агружает tempdb
*/
SELECT COUNT(*) AS LinesCountAfter
	FROM AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByBeginDate
		WHERE BeginDate >= @begindate AND BeginDate <= @enddate  -- «агружает tempdb
