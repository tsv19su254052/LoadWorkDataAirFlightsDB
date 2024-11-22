-- �������� �������� �� ���� ������������� � ������� ���� ���������

DECLARE @begindate DATE, @enddate DATE, @currentdate DATE, @rt BIGINT, @ac BIGINT, @reg VARCHAR(50), @acnew BIGINT, @fns VARCHAR(50), @q BIGINT, @fd DATE, @bd DATE, @ReturnValue INT, @fails BIGINT
SET @begindate = '2024-04-01'
SET @enddate = '2024-05-01'
SET @currentdate = @begindate
SET @fails = 0

-- ������� �������
SET Transaction Isolation Level Read Committed
SELECT COUNT(*) AS LinesCountTotal
	FROM AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByBeginDate  -- ��������� tempdb

SET Transaction Isolation Level Serializable
WHILE @currentdate <= @enddate
	-- �������� �� ������ ������ ���� (����� ���������� ��� �������� - 56 ... 58 ���, � ��������� - 18 �����)
	BEGIN
		DECLARE cursor_flight CURSOR FORWARD_ONLY STATIC FOR
			SELECT	AirRoute,
					AirCraft,
					FlightNumberString,  -- �������� ���� �������������� Unicode -> cp-1251
					QuantityCounted,
					FlightDate,
					BeginDate
					FROM AirFlightsDBNew72WorkBase.dbo.AirFlightsTable
						WHERE AirFlightsDBNew72WorkBase.dbo.AirFlightsTable.BeginDate = @currentdate
							ORDER BY AirCraft, FlightNumberString
		PRINT ' + ������ ��������'

		OPEN cursor_flight  -- ��������� ��������� ���� �����
		FETCH NEXT FROM cursor_flight INTO @rt, @ac, @fns, @q, @fd, @bd  -- ���������� �� ������ ������ � ����������� �� ����������

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
					AirRoute,  -- BIGINT NOT NULL, ������� ������
					AirCraft,  -- BIGINT NOT NULL - ������� ���� �� ����������� ��������, ������� ������
					FlightNumberString,  -- VARCHAR(50) NOT NULL, ������� ������
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
				FETCH NEXT FROM cursor_flight
				INTO @rt, @ac, @fns, @q, @fd, @bd
			END
		CLOSE cursor_flight
		DEALLOCATE cursor_flight

		-- PRINT ' + date = ' + CONVERT(VARCHAR(100), @currentdate)
		SELECT	@currentdate AS CurrentMonth,
				COUNT(*) AS LinesCount
			FROM AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByBeginDate
				WHERE BeginDate = @currentdate  -- ��������� tempdb
		SET @currentdate = DATEADD(MONTH, 1, @currentdate)
	END

PRINT ' + �������� �����������, ������� = ' +  CONVERT(VARCHAR(100), @fails)

-- ��������� � ���������� ��� � ������� ����������
/*
SET Transaction Isolation Level Read Committed  -- Ckbirjv vyjuj -> ������ �����
SELECT COUNT(*) AS LinesCountAllMonthsBefore
	FROM AirFlightsDBNew72WorkBase.dbo.AirFlightsTable
		WHERE AirFlightsDBNew72WorkBase.dbo.AirFlightsTable.BeginDate >= @begindate AND AirFlightsDBNew72WorkBase.dbo.AirFlightsTable.BeginDate <= @enddate  -- ��������� tempdb
*/
SELECT COUNT(*) AS LinesCountAfter
	FROM AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByBeginDate
		WHERE BeginDate >= @begindate AND BeginDate <= @enddate  -- ��������� tempdb
