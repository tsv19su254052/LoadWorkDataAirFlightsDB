USE AirPortsAndRoutesDBNew62
GO

DECLARE @iata NVARCHAR(50)
SET @iata = 'CKL'

SELECT	* 
  FROM dbo.AirPortsTable
	WHERE AirPortCodeIATA = @iata
		ORDER BY AirPortCodeIATA, AirPortCodeICAO

-- UPDATE dbo.AirPortsTable SET AirPortCodeICAO = 'UBBL' WHERE AirPortUniqueNumber = 9554

SELECT	* 
  FROM dbo.AirPortsTable
	WHERE AirPortCodeIATA = @iata
		ORDER BY AirPortCodeIATA, AirPortCodeICAO
