USE AirPortsAndRoutesDBNew62
GO

DECLARE @Name1 VARCHAR(100), @Name2 VARCHAR(100), @Name3 VARCHAR(100),@Name4 VARCHAR(100), @Name5 VARCHAR(100)
SET @Name1 = 'Sergey'
SET @Name2 = 'Andrey'
SET @Name3 = 'Sasha'
SET @Name4 = 'Teslikov_V'
SET @Name5 = 'Hramushin'

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
SELECT	@Name1,
		HyperLinkToWikiPedia,
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
	WHERE LogDateAndTimeViewed.exist('/Viewed/User[@Name=sql:variable("@Name1")] ') = 1  -- есть просмотры
		ORDER BY AirPortCodeIATA, AirPortCodeICAO

SELECT	@Name2,
		HyperLinkToWikiPedia,
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
	WHERE LogDateAndTimeViewed.exist('/Viewed/User[@Name=sql:variable("@Name2")] ') = 1  -- есть просмотры
		ORDER BY AirPortCodeIATA, AirPortCodeICAO

SELECT	@Name3,
		HyperLinkToWikiPedia,
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
	WHERE LogDateAndTimeViewed.exist('/Viewed/User[@Name=sql:variable("@Name3")] ') = 1  -- есть просмотры
		ORDER BY AirPortCodeIATA, AirPortCodeICAO

SELECT	@Name4,
		HyperLinkToWikiPedia,
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
	WHERE LogDateAndTimeViewed.exist('/Viewed/User[@Name=sql:variable("@Name4")] ') = 1  -- есть просмотры
		ORDER BY AirPortCodeIATA, AirPortCodeICAO

SELECT	@Name5,
		HyperLinkToWikiPedia,
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
	WHERE LogDateAndTimeViewed.exist('/Viewed/User[@Name=sql:variable("@Name5")] ') = 1  -- есть просмотры
		ORDER BY AirPortCodeIATA, AirPortCodeICAO

