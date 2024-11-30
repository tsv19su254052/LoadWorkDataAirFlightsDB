USE AirPortsAndRoutesDBNew62
GO

DECLARE @iata NCHAR(10), @icao NCHAR(10), @User NVARCHAR(100), @Host NVARCHAR(100)
SET @iata = 'LAX'
SET @icao = 'KLAX'
SET @User = 'Sasha'

/*
SET Transaction Isolation Level Repeatable Read
UPDATE dbo.AirPortsTable SET AirPortGeo = geography::STPointFromText(CONCAT('POINT(', (SELECT AirPortLongitude FROM dbo.AirPortsTable WHERE AirPortCodeIATA = @iata AND AirPortCodeICAO = @icao),
																			' ', (SELECT AirPortLatitude FROM dbo.AirPortsTable WHERE AirPortCodeIATA = @iata AND AirPortCodeICAO = @icao), ') '), 4326) 
	WHERE AirPortCodeIATA = @iata AND AirPortCodeICAO = @icao
*/

-- Выставляем всем географические координаты
SET Transaction Isolation Level Repeatable Read
UPDATE dbo.AirPortsTable SET AirPortGeo = geography::STPointFromText(CONCAT('POINT(', AirPortLongitude, ' ', AirPortLatitude, ') '), 4326) 
	WHERE AirPortCodeIATA IS NOT NULL AND AirPortCodeICAO IS NOT NULL

-- UPDATE dbo.AirRoutesTable SET Distance = geography::STGeomFromText('LINESTRING(-122.360 47.656, -122.343 47.656)', 4326)
