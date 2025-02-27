USE AirCraftsDBNew62
GO
/****** Object:  StoredProcedure [dbo].[SPInsertUpdateAirCraftByData]    Script Date: 01.05.2021 9:56:04 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Тарасов СЕРГЕЙ
-- Create date:	01 мая 2021 года
-- Изменено:	11 января 2024 года
-- Description:	Обновление данных самолета
-- =============================================
CREATE PROCEDURE [dbo].[SPUpdateAirCraftRegistrationXMLByLNAndMSN] (@registration VARCHAR(50), @BeginDate DATE, @LN VARCHAR(50), @MSN VARCHAR(50), @SN VARCHAR(50), @CN VARCHAR(50))
AS
BEGIN
	-- Тело процедуры
	SET XACT_ABORT ON -- закрываем открытые безхозные транзакции, исходя из того, что одновременно пусть будет открыта только одна транзакция
	SET NOCOUNT ON; -- снимаем ограничение "row(s) affected", SET NOCOUNT ON added to prevent extra result sets from
	-- Тело процедуры
	BEGIN TRY
		-- Первичный ключ уникален, но присваивается автоинкрементом в разных сессиях и поэтому возможны разрывы в сквозной нумерации
		-- Каскадные правила на UPDATE и DELETE 
		DECLARE @TransactionName VARCHAR(32)
		SET @TransactionName = CONCAT('TA_CountOf_', @LN, '_', @MSN)  -- используются <= 32 символов
		SET Transaction Isolation Level Repeatable Read
		BEGIN TRANSACTION @TransactionName WITH MARK  -- пометка транзакции (работает с SQL Server 2008-го)
			IF EXISTS(SELECT * FROM dbo.AirCraftsTableNew2Xsd WHERE AirCraftLineNumber_LN = @LN AND AirCraftLineNumber_MSN = @MSN)
				BEGIN
					-- Обновляем поле регистрации с датой, указанной на входе процедуры
					DECLARE @XmlQuery XML
					SET @XmlQuery = (SELECT AirCraftRegistration FROM dbo.AirCraftsTableNew2Xsd WHERE AirCraftLineNumber_LN = @LN AND AirCraftLineNumber_MSN = @MSN)
					IF (SELECT @XmlQuery.exist('/CustReg/step[@CraftRegFK=sql:variable("@registration")] ')) = 0
						BEGIN
							SET @XmlQuery.modify('insert <step> CraftRegFK=sql:variable("@registration") </step> into (/CustReg)[1] ')
						END
					-- Проверяем наличие этой даты в списке дат элемента с атрибутом этой регистрации
					IF (SELECT @XmlQuery.exist('/CustReg/step[@CraftRegFK=sql:variable("@registration")]/BeginDate=sql:variable("@BeginDate") ')) = 0
						BEGIN
							SET @XmlQuery.modify('insert <BeginDate> sql:variable("@BeginDate") </BeginDate> into (/CustReg/step[@CraftRegFK=sql:variable("@registration")])[1] ')
							UPDATE dbo.AirCraftsTableNew2Xsd SET AirCraftRegistration = @XmlQuery, AirCraftSerialNumber_SN = @SN, AirCraftCNumber_CN = @CN
								WHERE AirCraftLineNumber_LN = @LN AND AirCraftLineNumber_MSN = @MSN
						END
					ELSE
						BEGIN
							PRINT 'Дата уже есть'
						END
				END
			ELSE
				BEGIN
					PRINT 'Строка с такими LN и MSN не найдена'
				END
		COMMIT TRANSACTION @TransactionName
	END TRY

	-- Обработка исключения
	BEGIN CATCH
		IF @@trancount > 0 ROLLBACK TRANSACTION  -- это откат всей процедуры, не "RowInsertionWithParam"
		DECLARE @msg NVARCHAR(2048) = error_message() -- текст ошибки
		RAISERROR (@msg, 16, 1)
		RETURN 55555 -- просто страховка для SQL Server 2005  и более ранних (не использовать в триггерах)
		PRINT ' -- не сработка'
	END CATCH

	SET Transaction Isolation Level Read Committed
	PRINT @TransactionName
	-- Выключаем обратно
	SET XACT_ABORT OFF
	SET NOCOUNT OFF
END
