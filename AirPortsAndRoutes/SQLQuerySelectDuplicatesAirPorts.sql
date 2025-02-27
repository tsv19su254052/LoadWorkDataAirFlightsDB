USE AirPortsAndRoutesDBNew62
GO
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT	AirPortName, 
		AirPortCodeIATA, 
		AirPortCodeICAO, 
		COUNT(*) AS Duplicates
  FROM AirPortsTable
	GROUP BY	AirPortName, 
				AirPortCodeIATA,
				AirPortCodeICAO
	HAVING COUNT(*) > 1 -- 2 шт. с дубликатами - оставил только первые, остальные удалил