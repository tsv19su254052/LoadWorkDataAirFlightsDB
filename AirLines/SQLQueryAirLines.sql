-- :CONNECT data-server-1.movistar.vrn.skylink.local
-- :CONNECT terminalserver\mssqlserver15
USE AirLinesDBNew62
GO

SET STATISTICS XML ON
SET Transaction Isolation Level Read Committed
SELECT * FROM dbo.AirLinesView
  ORDER BY AirLineCodeIATA, AirLineCodeICAO  -- 7209

SELECT AirLineName, AirLineCodeIATA, AirLineCodeICAO,  COUNT(*) AS Duplicates
  FROM dbo.AirLinesTable
  GROUP BY AirLineName, AirLineCodeIATA, AirLineCodeICAO
  HAVING COUNT(*) > 1 -- (63 -> __) авиакомпаний с дубликатами по кодам IATA и ICAO, были по 3 ... 4 строки
  ORDER BY AirLineCodeIATA, AirLineCodeICAO

SELECT  dbo.AlliancesTable.AllianceName, 
		dbo.AirLinesTable.AirLineName, 
		dbo.AirLinesTable.AirLineAlias, 
		dbo.AirLinesTable.AirLineCodeIATA, 
		dbo.AirLinesTable.AirLineCodeICAO, 
		dbo.AirLinesTable.AirLine_ID, 
		dbo.AirLinesTable.AirLineCallSighn, 
		dbo.AirLinesTable.AirLineCountry, 
		dbo.AirLinesTable.AirLineStatus, 
		dbo.AirLinesTable.CreationDate, 
		-- dbo.AirLinesTable.AirLineDescription,
		dbo.AirLinesTable.Hubs
FROM dbo.AirLinesTable INNER JOIN dbo.AlliancesTable ON dbo.AirLinesTable.Alliance = dbo.AlliancesTable.AllianceUniqueNumber
  -- WHERE AllianceName = 'ASL Aviation Holdings DAC'
  -- WHERE dbo.AirLinesTable.AirLineCodeIATA = 'AK' OR dbo.AirLinesTable.AirLineCodeICAO = 'ALT'
  WHERE AirLineCodeIATA IS NULL OR AirLineCodeICAO IS NULL
  ORDER BY AirLineCodeIATA, AirLineCodeICAO
GO