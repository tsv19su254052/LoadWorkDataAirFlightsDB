USE AirFlightsDBNew72WorkBase
GO

-- ������� ��������� �����
SET Transaction Isolation Level Read Committed
SELECT * 
  FROM AirFlightsTable
  ORDER BY FlightDate
GO

  --  ������� ��� ������ � ��������� ���� �������
SET Transaction Isolation Level Serializable
-- DELETE FROM dbo.AirFlightsTable
-- WHERE FlightDescription LIKE '+++_T_ONTIME_REPORTING_1987_11.csv'
GO

-- ��� ��� ������� ��������� �����
SET Transaction Isolation Level Read Committed
SELECT * 
  FROM AirFlightsTable
  ORDER BY FlightDate
GO
