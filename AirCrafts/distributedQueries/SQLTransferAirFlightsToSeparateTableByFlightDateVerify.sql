DECLARE @begindate DATE, @enddate DATE, @currentdate DATE
-- ���� �������� ��� ��� �����������
SET @begindate = '2012-01-01'
SET @enddate = '2012-12-31'

-- ���������
-- ������� ����
SET Transaction Isolation Level Read Committed
SELECT COUNT(*) AS LinesCountFromAirFlights
	FROM AirFlightsDBNew72WorkBase.dbo.AirFlightsTable
		WHERE FlightDate BETWEEN @begindate AND @enddate  -- ��������� tempdb
-- � ������� ����������
SELECT COUNT(*) AS LinesCountFromAirCrafts
	FROM AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByFlightDate
		WHERE FlightDate >= @begindate AND FlightDate <= @enddate  -- ��������� tempdb
-- ������ ������ �� AirFlightsDBNew72WorkBase.dbo.AirFlightsTable.FlightDate -> � 3 ���� �������
