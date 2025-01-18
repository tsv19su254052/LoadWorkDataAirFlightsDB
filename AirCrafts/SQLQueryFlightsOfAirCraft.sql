USE AirCraftsDBNew62
GO

DECLARE @Reg1 VARCHAR(50), @Reg2 VARCHAR(50), @Reg3 VARCHAR(50), @Reg4 VARCHAR(50), @Reg5 VARCHAR(50), @Reg6 VARCHAR(50), @Reg7 VARCHAR(50), @Reg8 VARCHAR(50)
-- 10876
SET @Reg1 = 'N67158'	-- 18, 4 -> 37, 0 -> 106, 0 -> 119 (1505)
SET @Reg2 = 'N68160'	-- 16, 3 -> 37, 0 -> 103, 0 -> 123 (1643)
SET @Reg3 = 'N76156'	-- 12, 2 -> 36, 0 -> 97, 0 -> 116 (1581)
SET @Reg4 = 'N2DCAA'	-- 8416, 160 -> 9265, 0 -> 10258, 0 -> 10319 (10323 - было много несработок)
SET @Reg5 = 'N2BYAA'	-- 8469, 156 -> 9372, 0 -> 10327, 0 -> 10379 (11926 - было много несработок)
SET @Reg6 = 'nan'		-- 3581, 1321 -> 6918, 1321 -> 20992, 1320 -> 41074, 1320 (980614)
SET @Reg7 = 'Unknow'	-- 536198, 685 -> 572299, 0 (572311)
SET @Reg8 = 'Unknown'	-- пусто

/*
Вывод:
большие самолеты American AirLines, Continental как правило более привязаны к маршруту
	UTair Boeing 767-224(ER):
	- N67158 (Continental AirLines 30.05.2001 -> United Airlines 01.12.2011) -> VP-BAI -> RA-73082 (UTair Aviation) https://www.airfleets.net/ficheapp/plane-b767-30437.htm
	- N68160 (Continental AirLines 30.10.2001 -> United Airlines 01.12.2011) -> VP-BAL -> RA-73083 (UTair Aviation) https://www.airfleets.net/ficheapp/plane-b767-30439.htm
	- N76156 (Continental AirLines 15.02.2001, United Airlines 01.12.2011) -> VP-BAG -> RA-73081 (UTair Aviation) https://www.airfleets.net/ficheapp/plane-b767-30435.htm
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
