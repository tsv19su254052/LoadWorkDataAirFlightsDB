-- � ���� ��������� �������� �������� �� ������� ��������� � ������ FlightsByRoutes ������� �����������
-- fixme SSMS ������ ��������� � ������� �� 125 ������
DECLARE @begindate DATE, @enddate DATE, @currentdate DATE
SET @begindate = '2002-05-01'
SET @enddate = '2002-05-31'
SET NOCOUNT ON  -- ������� ������ ��������� � ���������� ������� -> fixme SSMS ������� 122 ������ � �������
SET Transaction Isolation Level Repeatable Read
SET @currentdate = @begindate
WHILE @currentdate <= @enddate
	BEGIN
		DECLARE @rt BIGINT, @ac BIGINT, @reg VARCHAR(50), @fns VARCHAR(50), @q BIGINT, @fd DATE, @bd DATE, @inserted BIGINT, @added BIGINT, @padded BIGINT, @fails BIGINT
		SET @inserted = 0
		SET @added = 0
		SET @padded = 0
		SET @fails = 0
		DECLARE cursor_flightByRoute CURSOR FORWARD_ONLY STATIC FOR  -- ����������� ���������������� (����� �������)
			SELECT	AirRoute,
					AirCraft,
					FlightNumberString,
					QuantityCounted,
					FlightDate,
					BeginDate
				FROM AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByFlightDate
					WHERE FlightDate = @currentdate
						ORDER BY AirCraft, FlightNumberString
		PRINT ' + ������ ��������'
		-- ��������� ��������� ���� ����� � tempdb (��� ���������� ��� ��������� ��������)
		OPEN cursor_flightByRoute
		-- ���������� �� ������ ������ � ������ � ����������� �� ����������
		FETCH NEXT FROM cursor_flightByRoute INTO @rt, @ac, @fns, @q, @fd, @bd  
		WHILE @@FETCH_STATUS = 0
			-- ����� ���������� �� ����� ������ � �����
			BEGIN
				SET @reg = (SELECT AirCraftRegistration FROM AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate WHERE AirCraftUniqueNumber = @ac)
				-- ��������� QuantityCounted
				DECLARE @counter BIGINT
				SET @counter = @q
				WHILE @counter >= 1
					BEGIN
						DECLARE @RetryCount INT 
						SET @RetryCount = 750  -- ����� �������
						-- ���� �������
						WHILE @RetryCount >= 0
							BEGIN
								DECLARE @ReturnValue INT
								EXECUTE @ReturnValue = AirCraftsDBNew62.dbo.SPFlightInsertOrUpdate @reg, @fns, @rt, @fd, @bd
								IF @ReturnValue = 0
									SET @fails += 1  -- ����������
								IF @ReturnValue = 3
									BEGIN
										SET @inserted += 1
										BREAK
									END
								IF @ReturnValue = 1
									BEGIN
										SET @added += 1
										BREAK
									END
								IF @ReturnValue = 2
									BEGIN
										SET @padded += 1
										BREAK
									END
								SET @RetryCount -= 1
							END
						SET @counter -= 1
					END
				FETCH NEXT FROM cursor_flightByRoute
				INTO @rt, @ac, @fns, @q, @fd, @bd
			END
		CLOSE cursor_flightByRoute
		DEALLOCATE cursor_flightByRoute
		SELECT	@currentdate AS CurrentDate,
				COUNT(*) AS LinesCount,
				@inserted AS LinesInserted,
				@added AS LinesAdded,
				@padded AS LinesPadded,
				@fails AS FailedPoints
			FROM AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByFlightDate
				WHERE FlightDate = @currentdate  -- ��������� tempdb
		SET @currentdate = DATEADD(DAY, 1, @currentdate)
	END
-- ������� �����
SET Transaction Isolation Level Read Committed
SELECT COUNT(*) AS LinesCountTotal
	FROM AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByFlightDate  -- ��������� tempdb
SET NOCOUNT OFF
