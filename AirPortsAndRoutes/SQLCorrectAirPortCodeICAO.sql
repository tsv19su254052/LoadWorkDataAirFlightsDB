USE AirPortsAndRoutesDBNew62
GO

DECLARE @iata NVARCHAR(50)
SET @iata = 'OVS'

SELECT	* 
  FROM dbo.AirPortsTable
	WHERE AirPortCodeIATA = @iata
		ORDER BY AirPortCodeIATA, AirPortCodeICAO

UPDATE dbo.AirPortsTable SET AirPortCodeICAO = 'USHS' WHERE AirPortUniqueNumber = 9609

SELECT	* 
  FROM dbo.AirPortsTable
	WHERE AirPortCodeIATA = @iata
		ORDER BY AirPortCodeIATA, AirPortCodeICAO
