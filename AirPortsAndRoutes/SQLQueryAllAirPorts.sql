USE AirPortsAndRoutesDBNew62
GO

DECLARE @Name NVARCHAR(50)
SET @Name = 'Sergey'  -- остальные учетки такие: Sergey, Andrey, Sasha, Teslikov_V, Hramushin

SELECT	AirPortCodeIATA,
		AirPortCodeICAO,
		AirPortCodeFAA_LID,
		AirPortCodeWMO,
		AirPortName,
		AirPortCity,
		AirPortGeo.ToString() AS GeoCoordinates,
		LogCountViewed,
		LogDateAndTimeViewed,
		LogCountChanged,
		LogDateAndTimeChanged FROM dbo.AirPortsTable
	WHERE LogDateAndTimeViewed IS NOT NULL
		ORDER BY AirPortCodeIATA, AirPortCodeICAO

SET Transaction Isolation Level Read Committed
SELECT	HyperLinkToWikiPedia,
		HyperLinkToAirPortSite,
		HyperLinkToOperatorSite,
		AirPortCodeIATA,
		AirPortCodeICAO,
		AirPortCodeFAA_LID,
		AirPortCodeWMO,
		AirPortName,
		AirPortLatitude,
		AirPortLongitude,
		AirPortGeo.ToString() AS GeoCoordinates,
		LogCountViewed,
		LogDateAndTimeViewed,
		LogCountChanged,
		LogDateAndTimeChanged
  FROM dbo.AirPortsTable
	WHERE LogDateAndTimeViewed.exist('/Viewed/User[@Name=sql:variable("@Name")] ') = 1  -- есть просмотры
		ORDER BY AirPortCodeIATA, AirPortCodeICAO

