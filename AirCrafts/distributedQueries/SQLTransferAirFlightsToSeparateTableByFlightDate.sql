-- �������� �������� �� ���� ������������� � ������� ���� ���������
DECLARE @begindate DATE, @enddate DATE, @currentdate DATE
-- ���� �������� ��� ��� �����������
SET @begindate = '2024-01-01'
SET @enddate = '2024-12-31'
SET @currentdate = @begindate
-- ������� �������
SET Transaction Isolation Level Read Committed
SELECT COUNT(*) AS LinesCountTotal
	FROM AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByFlightDate  -- ��������� tempdb
SET Transaction Isolation Level Serializable
WHILE @currentdate <= @enddate
	BEGIN
		DECLARE @rt BIGINT, @ac BIGINT, @acnew BIGINT, @fns VARCHAR(50), @q BIGINT, @fd DATE, @bd DATE, @fails BIGINT
		SET @fails = 0
		DECLARE cursor_flight CURSOR FORWARD_ONLY STATIC FOR
			SELECT	AirRoute,
					AirCraft,
					FlightNumberString,
					QuantityCounted,
					FlightDate,
					BeginDate
				FROM AirFlightsDBNew72WorkBase.dbo.AirFlightsTable
					WHERE FlightDate = @currentdate
						ORDER BY AirCraft, FlightNumberString  -- �������� �� ���������
		PRINT ' + ������ ��������'
		OPEN cursor_flight  -- ��������� ��������� ���� �����
		FETCH NEXT FROM cursor_flight INTO @rt, @ac, @fns, @q, @fd, @bd  -- ���������� �� ������ ������ � ������������ �� �� ����������
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
				IF @acnew IS NULL
					SET @acnew = 3 -- ������������� ����������� 'UNKNOWN' (���� ������������ ������ �����)
				IF @q IS NULL OR @q = 0
					SET @q = 1
				IF @rt IS NOT NULL AND @fns IS NOT NULL
					BEGIN
						INSERT INTO AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByFlightDate (
							AirRoute,  -- BIGINT NOT NULL PRIMARY KEY - �������������� ������� ���� �� ������� � ������ ����
							AirCraft,  -- BIGINT NOT NULL - ������� ���� �� ����������� ��������
							FlightNumberString,  -- VARCHAR(50) NOT NULL
							QuantityCounted,  -- BIGINT
							FlightDate,  -- DATE
							BeginDate,  -- DATE
							LoadDate) VALUES (@rt, @acnew, @fns, @q, @fd, @bd, GETDATE())
						/*
						SET @reg = (SELECT AirCraftRegistration FROM AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate WHERE AirCraftUniqueNumber = @acnew)
						EXECUTE @ReturnValue = AirCraftsDBNew62.dbo.SPFlightInsertOrUpdate @reg, @fns, @rt, @fd, @bd  -- ���� ������ ��-�� ����������������
						IF @ReturnValue = 0
							SET @fails += 1
						*/
					END
				ELSE 
					SET @fails += 1
				FETCH NEXT FROM cursor_flight
				INTO @rt, @ac, @fns, @q, @fd, @bd
			END
		CLOSE cursor_flight
		DEALLOCATE cursor_flight
		SELECT	@currentdate AS CurrentDate,
				COUNT(*) AS LinesCount,
				@fails AS FailedPoints
			FROM AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByFlightDate
				WHERE FlightDate = @currentdate  -- ��������� tempdb
		SET @currentdate = DATEADD(DAY, 1, @currentdate)  -- � ����� � 1 ����
	END

-- ���������
-- ������� ����
SET Transaction Isolation Level Read Committed
SELECT COUNT(*) AS LinesCountFromAirFlights
	FROM AirFlightsDBNew72WorkBase.dbo.AirFlightsTable
		WHERE FlightDate BETWEEN @begindate AND @enddate  -- ��������� tempdb
-- � ������� ����������
SELECT COUNT(*) AS LinesCountFromAirCrafts
	FROM AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByFlightDate
		WHERE FlightDate BETWEEN @begindate AND @enddate  -- ��������� tempdb
-- ������ ������ �� AirFlightsDBNew72WorkBase.dbo.AirFlightsTable.FlightDate -> � 3 ���� �������
