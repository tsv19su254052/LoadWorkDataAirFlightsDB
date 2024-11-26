USE AirCraftsDBNew62
GO

DECLARE @Reg1 VARCHAR(50), @Reg2 VARCHAR(50), @Reg3 VARCHAR(50), @Reg4 VARCHAR(50), @Reg5 VARCHAR(50), @Reg6 VARCHAR(50), @Reg7 VARCHAR(50), @Reg8 VARCHAR(50)
-- Регистрации с наиболее частыми несработками
SET @Reg1 = 'N2BYAA'
SET @Reg2 = 'N2DCAA'
SET @Reg3 = 'nan'
SET @Reg4 = 'Nan'
SET @Reg5 = 'NAN'
SET @Reg6 = 'Unknown'
SET @Reg7 = 'UNKNOW'
SET @Reg8 = 'UNKNOWN'

/*
Вывод:
большие самолеты American AirLines, Continental как правило более привязаны к маршруту
	UTair Boeing 767-224(ER):
	- N76156 (Continental AirLines 15.02.2001, United Airlines 01.12.2011) -> VP-BAG -> RA-73081 (UTair Aviation) https://www.airfleets.net/ficheapp/plane-b767-30435.htm
	- N67158 (Continental AirLines 30.05.2001 -> United Airlines 01.12.2011) -> VP-BAI -> RA-73082 (UTair Aviation) https://www.airfleets.net/ficheapp/plane-b767-30437.htm
	- N68160 (Continental AirLines 30.10.2001 -> United Airlines 01.12.2011) -> VP-BAL -> RA-73083 (UTair Aviation) https://www.airfleets.net/ficheapp/plane-b767-30439.htm
*/

SET Transaction Isolation Level Read Committed
-- Идея такая: 
	-- Разложить XML-ную ячейку с указанной регистрацией во временную таблицу (перед этим удалить из нее предыдущие строки), потом в эту таблицу подставить аэропорты
	-- Вывести авиаперелеты, не найденные в БД авиаперелетов
SELECT	AirCraftRegistration,
		-- Вставить сюда цикл на xQuery (XML с номерами маршрутов -> XML с названиями аэропортов), в который подставляю поля из подзапроса
		FlightsByRoutes,
		FlightsByRoutes.value('count(/FlightsByRoutes/Flight/Route/step)', 'BIGINT') AS CountOfFlights,
		FlightsByRoutes.query('for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes') AS EmptyRoutes,
		FlightsByRoutes.value('count(for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes)', 'BIGINT') AS CountOfEmptyRoutes,
		-- FlightsByRoutes.value('count(for $routes in /FlightsByRoutes/Flight/Route where $routes='' return $routes)', 'BIGINT') AS CountOfEmptyRoutes,  -- fixme  Незавершенная строковая константа (начало на строке 1)
		AirCraftLineNumber_LN_OLD AS LN_OLD,  -- Столбцы отсюда и ниже возможно недостоверны (данные с разных самолетов с одной регистрацией налазили друг на друга)
		AirCraftLineNumber_LN_NEW AS LN_NEW,
		AirCraftLineNumber_MSN AS MSN,
		AirCraftSerialNumber_SN AS SN,
		AirCraftCNumber_CN_OLD AS CN_OLD,
		AirCraftCNumber_CN_NEW AS CN_NEW,
		ManufacturerName,
		ModelName
	FROM AirCraftsTableNew2XsdIntermediate
		INNER JOIN AirCraftModelsTable ON AirCraftsTableNew2XsdIntermediate.AirCraftModel = AirCraftModelsTable.AirCraftModelUniqueNumber
		INNER JOIN AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
		WHERE FlightsByRoutes IS NOT NULL
			ORDER BY AirCraftRegistration

SELECT	AirCraftRegistration,
		FlightsByRoutes,
		FlightsByRoutes.value('count(/FlightsByRoutes/Flight/Route/step)', 'BIGINT') AS CountOfFlights,
		FlightsByRoutes.query('for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes') AS EmptyRoutes,
		FlightsByRoutes.value('count(for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes)', 'BIGINT') AS CountOfEmptyRoutes,
		AirCraftLineNumber_LN_OLD AS LN_OLD,  -- Столбцы отсюда и ниже возможно недостоверны (данные с разных самолетов с одной регистрвцией налазили друг на друга)
		AirCraftLineNumber_LN_NEW AS LN_NEW,
		AirCraftLineNumber_MSN AS MSN,
		AirCraftSerialNumber_SN AS SN,
		AirCraftCNumber_CN_OLD AS CN_OLD,
		AirCraftCNumber_CN_NEW AS CN_NEW,
		ManufacturerName,
		ModelName
	FROM AirCraftsTableNew2XsdIntermediate
		INNER JOIN AirCraftModelsTable ON AirCraftsTableNew2XsdIntermediate.AirCraftModel = AirCraftModelsTable.AirCraftModelUniqueNumber
		INNER JOIN AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
		WHERE AirCraftRegistration = @Reg1
			ORDER BY AirCraftRegistration

SELECT	AirCraftRegistration,
		FlightsByRoutes,
		FlightsByRoutes.value('count(/FlightsByRoutes/Flight/Route/step)', 'BIGINT') AS CountOfFlights,
		FlightsByRoutes.query('for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes') AS EmptyRoutes,
		FlightsByRoutes.value('count(for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes)', 'BIGINT') AS CountOfEmptyRoutes,
		AirCraftLineNumber_LN_OLD AS LN_OLD,  -- Столбцы отсюда и ниже возможно недостоверны (данные с разных самолетов с одной регистрвцией налазили друг на друга)
		AirCraftLineNumber_LN_NEW AS LN_NEW,
		AirCraftLineNumber_MSN AS MSN,
		AirCraftSerialNumber_SN AS SN,
		AirCraftCNumber_CN_OLD AS CN_OLD,
		AirCraftCNumber_CN_NEW AS CN_NEW,
		ManufacturerName,
		ModelName
	FROM AirCraftsTableNew2XsdIntermediate
		INNER JOIN AirCraftModelsTable ON AirCraftsTableNew2XsdIntermediate.AirCraftModel = AirCraftModelsTable.AirCraftModelUniqueNumber
		INNER JOIN AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
		WHERE AirCraftRegistration = @Reg2
			ORDER BY AirCraftRegistration

SELECT	AirCraftRegistration,
		FlightsByRoutes,
		FlightsByRoutes.value('count(/FlightsByRoutes/Flight/Route/step)', 'BIGINT') AS CountOfFlights,
		FlightsByRoutes.query('for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes') AS EmptyRoutes,
		FlightsByRoutes.value('count(for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes)', 'BIGINT') AS CountOfEmptyRoutes,
		AirCraftLineNumber_LN_OLD AS LN_OLD,  -- Столбцы отсюда и ниже возможно недостоверны (данные с разных самолетов с одной регистрвцией налазили друг на друга)
		AirCraftLineNumber_LN_NEW AS LN_NEW,
		AirCraftLineNumber_MSN AS MSN,
		AirCraftSerialNumber_SN AS SN,
		AirCraftCNumber_CN_OLD AS CN_OLD,
		AirCraftCNumber_CN_NEW AS CN_NEW,
		ManufacturerName,
		ModelName
	FROM AirCraftsTableNew2XsdIntermediate
		INNER JOIN AirCraftModelsTable ON AirCraftsTableNew2XsdIntermediate.AirCraftModel = AirCraftModelsTable.AirCraftModelUniqueNumber
		INNER JOIN AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
		WHERE AirCraftRegistration = @Reg3
			ORDER BY AirCraftRegistration

SELECT	AirCraftRegistration,
		FlightsByRoutes,
		FlightsByRoutes.value('count(/FlightsByRoutes/Flight/Route/step)', 'BIGINT') AS CountOfFlights,
		FlightsByRoutes.query('for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes') AS EmptyRoutes,
		FlightsByRoutes.value('count(for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes)', 'BIGINT') AS CountOfEmptyRoutes,
		AirCraftLineNumber_LN_OLD AS LN_OLD,  -- Столбцы отсюда и ниже возможно недостоверны (данные с разных самолетов с одной регистрвцией налазили друг на друга)
		AirCraftLineNumber_LN_NEW AS LN_NEW,
		AirCraftLineNumber_MSN AS MSN,
		AirCraftSerialNumber_SN AS SN,
		AirCraftCNumber_CN_OLD AS CN_OLD,
		AirCraftCNumber_CN_NEW AS CN_NEW,
		ManufacturerName,
		ModelName
	FROM AirCraftsTableNew2XsdIntermediate
		INNER JOIN AirCraftModelsTable ON AirCraftsTableNew2XsdIntermediate.AirCraftModel = AirCraftModelsTable.AirCraftModelUniqueNumber
		INNER JOIN AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
		WHERE AirCraftRegistration = @Reg4
			ORDER BY AirCraftRegistration

SELECT	AirCraftRegistration,
		FlightsByRoutes,
		FlightsByRoutes.value('count(/FlightsByRoutes/Flight/Route/step)', 'BIGINT') AS CountOfFlights,
		FlightsByRoutes.query('for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes') AS EmptyRoutes,
		FlightsByRoutes.value('count(for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes)', 'BIGINT') AS CountOfEmptyRoutes,
		AirCraftLineNumber_LN_OLD AS LN_OLD,  -- Столбцы отсюда и ниже возможно недостоверны (данные с разных самолетов с одной регистрвцией налазили друг на друга)
		AirCraftLineNumber_LN_NEW AS LN_NEW,
		AirCraftLineNumber_MSN AS MSN,
		AirCraftSerialNumber_SN AS SN,
		AirCraftCNumber_CN_OLD AS CN_OLD,
		AirCraftCNumber_CN_NEW AS CN_NEW,
		ManufacturerName,
		ModelName
	FROM AirCraftsTableNew2XsdIntermediate
		INNER JOIN AirCraftModelsTable ON AirCraftsTableNew2XsdIntermediate.AirCraftModel = AirCraftModelsTable.AirCraftModelUniqueNumber
		INNER JOIN AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
		WHERE AirCraftRegistration = @Reg5
			ORDER BY AirCraftRegistration

SELECT	AirCraftRegistration,
		FlightsByRoutes,
		FlightsByRoutes.value('count(/FlightsByRoutes/Flight/Route/step)', 'BIGINT') AS CountOfFlights,
		FlightsByRoutes.query('for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes') AS EmptyRoutes,
		FlightsByRoutes.value('count(for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes)', 'BIGINT') AS CountOfEmptyRoutes,
		AirCraftLineNumber_LN_OLD AS LN_OLD,  -- Столбцы отсюда и ниже возможно недостоверны (данные с разных самолетов с одной регистрвцией налазили друг на друга)
		AirCraftLineNumber_LN_NEW AS LN_NEW,
		AirCraftLineNumber_MSN AS MSN,
		AirCraftSerialNumber_SN AS SN,
		AirCraftCNumber_CN_OLD AS CN_OLD,
		AirCraftCNumber_CN_NEW AS CN_NEW,
		ManufacturerName,
		ModelName
	FROM AirCraftsTableNew2XsdIntermediate
		INNER JOIN AirCraftModelsTable ON AirCraftsTableNew2XsdIntermediate.AirCraftModel = AirCraftModelsTable.AirCraftModelUniqueNumber
		INNER JOIN AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
		WHERE AirCraftRegistration = @Reg6
			ORDER BY AirCraftRegistration

SELECT	AirCraftRegistration,
		FlightsByRoutes,
		FlightsByRoutes.value('count(/FlightsByRoutes/Flight/Route/step)', 'BIGINT') AS CountOfFlights,
		FlightsByRoutes.query('for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes') AS EmptyRoutes,
		FlightsByRoutes.value('count(for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes)', 'BIGINT') AS CountOfEmptyRoutes,
		AirCraftLineNumber_LN_OLD AS LN_OLD,  -- Столбцы отсюда и ниже возможно недостоверны (данные с разных самолетов с одной регистрвцией налазили друг на друга)
		AirCraftLineNumber_LN_NEW AS LN_NEW,
		AirCraftLineNumber_MSN AS MSN,
		AirCraftSerialNumber_SN AS SN,
		AirCraftCNumber_CN_OLD AS CN_OLD,
		AirCraftCNumber_CN_NEW AS CN_NEW,
		ManufacturerName,
		ModelName
	FROM AirCraftsTableNew2XsdIntermediate
		INNER JOIN AirCraftModelsTable ON AirCraftsTableNew2XsdIntermediate.AirCraftModel = AirCraftModelsTable.AirCraftModelUniqueNumber
		INNER JOIN AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
		WHERE AirCraftRegistration = @Reg7
			ORDER BY AirCraftRegistration

SELECT	AirCraftRegistration,
		FlightsByRoutes,
		FlightsByRoutes.value('count(/FlightsByRoutes/Flight/Route/step)', 'BIGINT') AS CountOfFlights,
		FlightsByRoutes.query('for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes') AS EmptyRoutes,
		FlightsByRoutes.value('count(for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes)', 'BIGINT') AS CountOfEmptyRoutes,
		AirCraftLineNumber_LN_OLD AS LN_OLD,  -- Столбцы отсюда и ниже возможно недостоверны (данные с разных самолетов с одной регистрвцией налазили друг на друга)
		AirCraftLineNumber_LN_NEW AS LN_NEW,
		AirCraftLineNumber_MSN AS MSN,
		AirCraftSerialNumber_SN AS SN,
		AirCraftCNumber_CN_OLD AS CN_OLD,
		AirCraftCNumber_CN_NEW AS CN_NEW,
		ManufacturerName,
		ModelName
	FROM AirCraftsTableNew2XsdIntermediate
		INNER JOIN AirCraftModelsTable ON AirCraftsTableNew2XsdIntermediate.AirCraftModel = AirCraftModelsTable.AirCraftModelUniqueNumber
		INNER JOIN AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
		WHERE AirCraftRegistration = @Reg8
			ORDER BY AirCraftRegistration
