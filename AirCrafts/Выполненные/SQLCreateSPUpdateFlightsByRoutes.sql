USE [AirCraftsDBNew62]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		������� ������
-- Create date:	01 ��� 2024 ����
-- Description:	������� ��� ���������� ������������� �������� ������ �� ���������
-- =============================================
CREATE PROCEDURE [dbo].[SPUpdateFlightsByRoutes] (@Reg NVARCHAR(50), @FNS NVARCHAR(100), @Route BIGINT, @FD DATE, @BD DATE)
AS
BEGIN
	-- ���� ���������
	SET XACT_ABORT ON -- ��������� �������� ��������� ����������, ������ �� ����, ��� ������������ ����� ����� ������� ������ ���� ����������
	SET NOCOUNT ON; -- ������� ����������� "row(s) affected", SET NOCOUNT ON added to prevent extra result sets from
	BEGIN TRY
		-- ��������� ���� ��������, �� ������������� ��������������� � ������ ������� � ������� �������� ������� � �������� ���������
		-- ��������� ������� �� UPDATE � DELETE 
		DECLARE @TransactionName VARCHAR(32)
		SET @TransactionName = CONCAT('Transaction_SelectCountOf_', @Route)  -- ������������ <= 32 ��������
		SET Transaction Isolation Level SERIALIZABLE
		BEGIN TRANSACTION @TransactionName WITH MARK  -- ������� ���������� (�������� � SQL Server 2008-��)
		--  �������� WITH UPDLOCK
		IF (SELECT FlightsByRoutes.exist('/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]') 
			FROM  AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = @Reg) = 1
			BEGIN
				PRINT '����� FlightNumberString ����'
				IF (SELECT FlightsByRoutes.exist('/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")]') 
					FROM  AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = @Reg) = 1
					BEGIN
						PRINT '����� ������� ����'
						IF (SELECT FlightsByRoutes.exist('/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")]/step[@FlightDate=sql:variable("@FD")]') 
							FROM  AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = @Reg) = 1
								PRINT '����� ���������� ����'
						ELSE
							BEGIN
								PRINT '��������� ���������� = ' + CONVERT(VARCHAR(100), @FD)
								-- UPDATE dbo.AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('insert <step FlightDate=sql:variable("@FD") BeginDate=sql:variable("@BD")> into (/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")])[1]') WHERE AirCraftRegistration = @Reg
							END
					END
				ELSE
					BEGIN
						PRINT '��������� ������� = ' + CONVERT(VARCHAR(100), @Route)  -- UPDATE 2 ���� ������ -> �������� ����� ������
						-- UPDATE dbo.AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('insert <Route RouteFK=sql:variable("@Route") BeginDate=sql:variable("@BD")> into (/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")])[1]') WHERE AirCraftRegistration = @Reg
						PRINT '��������� ���������� = ' + CONVERT(VARCHAR(100), @FD)
						-- UPDATE dbo.AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('insert <step FlightDate=sql:variable("@FD") BeginDate=sql:variable("@BD")> into (/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")])[1]') WHERE AirCraftRegistration = @Reg
					END
			END
		ELSE
			BEGIN
				PRINT '��������� FlightNumberString = ' + CONVERT(VARCHAR(100), @FNS)
				PRINT '��������� ������� = ' + CONVERT(VARCHAR(100), @Route)
				PRINT '��������� ���������� = ' + CONVERT(VARCHAR(100), @FD)
			END
		COMMIT TRANSACTION
	END TRY

	-- ��������� ����������
	BEGIN CATCH
		IF @@trancount > 0 ROLLBACK TRANSACTION  -- ��� ����� ���� ���������, �� "RowInsertionWithParam"
		DECLARE @msg NVARCHAR(2048) = error_message() -- ����� ������
		RAISERROR (@msg, 16, 1)
		RETURN 55555 -- ������ ��������� ��� SQL Server 2005  � ����� ������ (�� ������������ � ���������)
	END CATCH

	PRINT @TransactionName
	-- ��������� �������
	SET XACT_ABORT OFF
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT OFF
END
GO
