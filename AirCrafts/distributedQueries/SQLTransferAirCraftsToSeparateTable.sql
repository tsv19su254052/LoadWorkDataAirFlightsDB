-- Копируем данные по самолетам из базы авиаперелетов в отдельную таблицу
-- время выполнения 6 сек.

SET STATISTICS XML ON

/*
DECLARE @RemoteServer NVARCHAR(500)
SET @RemoteServer = 'data-server-1.movistar.vrn.skylink.local'

BEGIN TRY
	exec sp_addlinkedserver @server = @RemoteServer  -- срабатывает один раз, но иногда не с первого раза (лучше вынести в отдельный запрос) и работает на сеанс работы в SSMS, на следующие разы выдает ошибку
	PRINT ' Внешний сервер = ' + @RemoteServer + ' привязан'
END TRY
BEGIN CATCH
	PRINT ' Внешний сервер = ' + @RemoteServer + ' не привязался (уже привязан)'
END CATCH
*/

-- exec sp_linkedservers

SET Transaction Isolation Level Serializable
-- Первый вариант (без проверки существующих записей на дубликаты)

-- Удаляем промежуточную таблицу, если переделываем ее шапку (не всегда удаляется, удалить вручную)
DROP TABLE IF EXISTS AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate
PRINT ' Удалили промежуточную таблицу'

BEGIN TRY
	-- Очищаем промежуточную таблицу
	TRUNCATE TABLE AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate
	PRINT ' Промежуточная таблица очищена'
END TRY
BEGIN CATCH
	PRINT ' Делаем промежуточную таблицу'
	-- Делаем промежуточную таблицу (при внесении изменений в шапку таблицы раскомментировать удаление таблицы выше)
	CREATE TABLE AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate (
			AirCraftUniqueNumber BIGINT NOT NULL IDENTITY PRIMARY KEY, -- нужен в S.ModifyAirFlight
			AirCraftRegistration NVARCHAR(50),  -- Потом сделать вручную индекс
			FlightsByRoutes XML,
			AirCraftModel BIGINT DEFAULT 186 FOREIGN KEY REFERENCES AirCraftsDBNew62.dbo.AirCraftModelsTable(AirCraftModelUniqueNumber),  -- ключ не ставится -> Сделать вручную
			BuildDate DATE,  -- данные отсюда и ниже оставил, но они возможно не достоверны (разные самолеты с одной и той же регистрацией налазили друг на друга)
			RetireDate DATE,
			EndDate DATE,
			AirCraftLineNumber_LN_OLD NVARCHAR(50),
			AirCraftLineNumber_LN_NEW BIGINT,
			AirCraftLineNumber_MSN NVARCHAR(50),
			AirCraftSerialNumber_SN NVARCHAR(50),
			AirCraftCNumber_CN_OLD NVARCHAR(50),
			AirCraftCNumber_CN_NEW BIGINT,  -- не нужно (CN - произвольная текстовая строка)
			SourceCSVFile NTEXT,
			AirCraftDescription NTEXT)
	PRINT ' Промежуточная таблица сделана'
	-- Делаем первичный XML-ный индекс (см. стаью https://learn.microsoft.com/ru-ru/sql/relational-databases/xml/xml-indexes-sql-server?view=sql-server-ver16)
	CREATE PRIMARY XML INDEX PrimaryXML_IX_FlightsByRoutes ON AirCraftsTableNew2XsdIntermediate(FlightsByRoutes)
	-- На нем делаем вторичный XML-ный индекс
	CREATE XML INDEX PrimaryXML_IX_FlightsByRoutesPATH ON AirCraftsTableNew2XsdIntermediate(FlightsByRoutes)
	USING XML INDEX PrimaryXML_IX_FlightsByRoutes
	FOR PATH
	PRINT 'XML-ный (первичный и вторичный PATH) индекс сделан'
END CATCH

-- Копируем пригодные данные по самолетам из базы авиаперелетов в промежуточную таблицу
SET Transaction Isolation Level Serializable
-- BEGIN DISTRIBUTED TRANSACTION transferAirCrafts  -- ругается (см. снимок экрана)
	INSERT INTO AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate (
			AirCraftRegistration,
			AirCraftModel,
			BuildDate,
			RetireDate,
			EndDate,
			AirCraftLineNumber_LN_OLD,
			AirCraftLineNumber_LN_NEW,
			AirCraftSerialNumber_SN,
			AirCraftCNumber_CN_OLD,
			AirCraftCNumber_CN_NEW,
			SourceCSVFile,
			AirCraftDescription)
		SELECT AirCraftRegistration,
			(AirCraftModel + 201),  -- сдвиг на 201 в моделях самолетов
			BuildDate,
			RetireDate,
			EndDate,
			AirCraftLineNumber_LN_MSN,
			TRY_CAST(TRY_CAST(AirCraftLineNumber_LN_MSN AS FLOAT) AS BIGINT),  -- конвертировал в BIGINT, заменил 'nan' и все остальное на пустую ячейку
			AirCraftSerialNumber_SN,  -- в исходных данных буквы, цифры и спецсимволы
			AirCraftCNumber,
			TRY_CAST(TRY_CAST(AirCraftCNumber AS FLOAT) AS BIGINT),
			SourceCSVFile,
			AirCraftDescription
			FROM [data-server-1.movistar.vrn.skylink.local].AirFlightsDBNew62WorkBase.dbo.AirCraftsTable
-- COMMIT TRANSACTION

-- Второй вариант через временную таблицу (без проверки существующих записей на дубликаты) - НЕ ГОДИТСЯ

/*
SELECT	AirCraftRegistration,  -- преобразовать в XML-ное поле по ранее определенному шаблону
		(AirCraftModel + 201),  -- сдвиг на 201 в моделях самолетов
		BuildDate,  -- надо проверять тип данных
		RetireDate,  -- надо проверять тип данных
		SourceCSVFile,
		AirCraftDescription,
		AirCraftLineNumber_LN_MSN,  -- надо проверять тип данных, конвертировать в BIGINT, заменить 'nan' и все остальное на пустую ячейку -> СДЕЛАЛ
		AirCraftLineNumber_LN_NEW AS TRY_CAST(TRY_CAST(AirCraftLineNumber_LN_MSN AS FLOAT) AS BIGINT),  -- надо проверять тип данных, конвертировать в BIGINT, заменить 'nan' и все остальное на пустую ячейку -> СДЕЛАЛ
		AirCraftSerialNumber_SN,  -- надо проверять тип данных
		AirCraftCNumber,
		-- TRY_CONVERT(BIGINT, AirCraftCNumber),  -- надо проверять тип данных, конвертировать в BIGINT, заменить 'nan' и все остальное на пустую ячейку -> СДЕЛАЛ
		EndDate  -- надо проверять тип данных
	INTO  ##AirCraftsTableNew2XsdIntermediate  -- во временную таблицу (доступна для других запросов)
		FROM [data-server-1.movistar.vrn.skylink.local].AirFlightsDBNew62WorkBase.dbo.AirCraftsTable

SELECT * FROM ##AirCraftsTableNew2XsdIntermediate
*/
