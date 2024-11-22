USE AirPortsAndRoutesDBNew62
GO

SET Transaction Isolation Level Read Committed
SELECT * 
  FROM dbo.AirRoutesTable
	WHERE DistanceGeo IS NOT NULL
