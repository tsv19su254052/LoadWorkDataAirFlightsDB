USE AirCraftsDBNew62
GO

SET Transaction Isolation Level Read Committed
DECLARE @Reg VARCHAR(50), @faildate DATE
SET @Reg = 'N131EV'
SET @faildate = '2000-09-01'
-- смотрим указанный месяц
SELECT	AirCraftRegistration,
		-- FlightsByRoutes.value(('/FlightsByRoutes/Flight/Route/step/@BeginDate'), 'DATE') AS BEGINDATE,
		FlightsByRoutes.query('for $flights in /FlightsByRoutes/Flight where $flights/Route/step/@BeginDate = sql:variable("@faildate") return $flights') AS FlightsWithFailDateBefore
	FROM AirCraftsTableNew2XsdIntermediate
		INNER JOIN AirCraftModelsTable ON AirCraftsTableNew2XsdIntermediate.AirCraftModel = AirCraftModelsTable.AirCraftModelUniqueNumber
		INNER JOIN AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
		-- WHERE ModelName = 'DC-10'
		WHERE FlightsByRoutes.exist('/FlightsByRoutes/Flight/Route/step[@BeginDate = sql:variable("@faildate")]') = 1
			ORDER BY AirCraftRegistration

SET Transaction Isolation Level Read Committed
SELECT	AirCraftRegistration,
		-- FlightsByRoutes.value(('/FlightsByRoutes/Flight/Route/step/@BeginDate'), 'DATE') AS BEGINDATE,
		FlightsByRoutes.query('for $steps in /FlightsByRoutes/Flight/Route/step where $steps/@BeginDate = sql:variable("@faildate") return $steps') AS StepsWithFailDateOnlyBefore
	FROM AirCraftsTableNew2XsdIntermediate
		INNER JOIN AirCraftModelsTable ON AirCraftsTableNew2XsdIntermediate.AirCraftModel = AirCraftModelsTable.AirCraftModelUniqueNumber
		INNER JOIN AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
		-- WHERE ModelName = 'DC-10'
		WHERE FlightsByRoutes.exist('/FlightsByRoutes/Flight/Route/step[@BeginDate = sql:variable("@faildate")]') = 1
			ORDER BY AirCraftRegistration

SET Transaction Isolation Level Repeatable Read
  -- Стираем все 
-- UPDATE AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes = NULL

  -- Стираем все с указанной регистрацией
-- UPDATE AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes = NULL WHERE AirCraftRegistration = @Reg

  -- Стираем только авиаперелеты (маршруты, FlightNumberString-и если нужно) с указанной датой и с указанной регистрацией
-- UPDATE AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('delete /FlightsByRoutes/Flight/Route/step[@BeginDate = sql:variable("@faildate")]') WHERE FlightsByRoutes IS NOT NULL AND AirCraftRegistration = @Reg

  -- Стираем только авиаперелеты (маршруты, FlightNumberString-и если нужно) с указанной датой
UPDATE AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('delete /FlightsByRoutes/Flight/Route/step[@BeginDate = sql:variable("@faildate")]') WHERE FlightsByRoutes IS NOT NULL

-- UPDATE AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('for $steps in /FlightsByRoutes/Flight/Route/step where $steps/@BeginDate = sql:variable("@faildate") return (delete $steps)') WHERE FlightsByRoutes IS NOT NULL
-- UPDATE AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('delete //step[@BeginDate = sql:variable("@faildate")]')  -- XML Validation: Invalid content. Expected element(s): 'step'. Location: /*:FlightsByRoutes[1]/*:Flight[1]/*:Route[2]
-- UPDATE AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('for $steps in /FlightsByRoutes/Flight/Route/step where $steps/@BeginDate=sql:variable("@faildate") return (delete nodes /FlightsByRoutes/Flight/Route/step[@BeginDate = sql:variable("@faildate")])') WHERE FlightsByRoutes IS NOT NULL

-- проверяем
SET Transaction Isolation Level Read Committed
SELECT	AirCraftRegistration,
		-- FlightsByRoutes.value(('/FlightsByRoutes/Flight/Route/step/@BeginDate'), 'DATE') AS BEGINDATE,
		FlightsByRoutes.query('for $steps in /FlightsByRoutes/Flight/Route/step where $steps/@BeginDate = sql:variable("@faildate") return $steps') AS StepsWithFailDateOnlyAfter
	FROM AirCraftsTableNew2XsdIntermediate
		INNER JOIN AirCraftModelsTable ON AirCraftsTableNew2XsdIntermediate.AirCraftModel = AirCraftModelsTable.AirCraftModelUniqueNumber
		INNER JOIN AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
		-- WHERE ModelName = 'DC-10'
		WHERE FlightsByRoutes.exist('/FlightsByRoutes/Flight/Route/step[@BeginDate = sql:variable("@faildate")]') = 1  -- VARCHAR(50)
			ORDER BY AirCraftRegistration
