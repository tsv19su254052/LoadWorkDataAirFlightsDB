-- �������� ������ �� ��������� �� ���� ������������� � ��������� �������
-- ����� ���������� 6 ���.

SET STATISTICS XML ON

/*
DECLARE @RemoteServer NVARCHAR(500)
SET @RemoteServer = 'data-server-1.movistar.vrn.skylink.local'

BEGIN TRY
	exec sp_addlinkedserver @server = @RemoteServer  -- ����������� ���� ���, �� ������ �� � ������� ���� (����� ������� � ��������� ������) � �������� �� ����� ������ � SSMS, �� ��������� ���� ������ ������
	PRINT ' ������� ������ = ' + @RemoteServer + ' ��������'
END TRY
BEGIN CATCH
	PRINT ' ������� ������ = ' + @RemoteServer + ' �� ���������� (��� ��������)'
END CATCH
*/

-- exec sp_linkedservers

SET Transaction Isolation Level Serializable
-- ������ ������� (��� �������� ������������ ������� �� ���������)

-- ������� ������������� �������, ���� ������������ �� ����� (�� ������ ���������, ������� �������)
DROP TABLE IF EXISTS AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate
PRINT ' ������� ������������� �������'

BEGIN TRY
	-- ������� ������������� �������
	TRUNCATE TABLE AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate
	PRINT ' ������������� ������� �������'
END TRY
BEGIN CATCH
	PRINT ' ������ ������������� �������'
	-- ������ ������������� ������� (��� �������� ��������� � ����� ������� ����������������� �������� ������� ����)
	CREATE TABLE AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate (
			AirCraftUniqueNumber BIGINT NOT NULL IDENTITY PRIMARY KEY, -- ����� � S.ModifyAirFlight
			AirCraftRegistration NVARCHAR(50),  -- ����� ������� ������� ������
			FlightsByRoutes XML,
			AirCraftModel BIGINT DEFAULT 186 FOREIGN KEY REFERENCES AirCraftsDBNew62.dbo.AirCraftModelsTable(AirCraftModelUniqueNumber),  -- ���� �� �������� -> ������� �������
			BuildDate DATE,  -- ������ ������ � ���� �������, �� ��� �������� �� ���������� (������ �������� � ����� � ��� �� ������������ �������� ���� �� �����)
			RetireDate DATE,
			EndDate DATE,
			AirCraftLineNumber_LN_OLD NVARCHAR(50),
			AirCraftLineNumber_LN_NEW BIGINT,
			AirCraftLineNumber_MSN NVARCHAR(50),
			AirCraftSerialNumber_SN NVARCHAR(50),
			AirCraftCNumber_CN_OLD NVARCHAR(50),
			AirCraftCNumber_CN_NEW BIGINT,  -- �� ����� (CN - ������������ ��������� ������)
			SourceCSVFile NTEXT,
			AirCraftDescription NTEXT)
	PRINT ' ������������� ������� �������'
	-- ������ ��������� XML-��� ������ (��. ����� https://learn.microsoft.com/ru-ru/sql/relational-databases/xml/xml-indexes-sql-server?view=sql-server-ver16)
	CREATE PRIMARY XML INDEX PrimaryXML_IX_FlightsByRoutes ON AirCraftsTableNew2XsdIntermediate(FlightsByRoutes)
	-- �� ��� ������ ��������� XML-��� ������
	CREATE XML INDEX PrimaryXML_IX_FlightsByRoutesPATH ON AirCraftsTableNew2XsdIntermediate(FlightsByRoutes)
	USING XML INDEX PrimaryXML_IX_FlightsByRoutes
	FOR PATH
	PRINT 'XML-��� (��������� � ��������� PATH) ������ ������'
END CATCH

-- �������� ��������� ������ �� ��������� �� ���� ������������� � ������������� �������
SET Transaction Isolation Level Serializable
-- BEGIN DISTRIBUTED TRANSACTION transferAirCrafts  -- �������� (��. ������ ������)
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
			(AirCraftModel + 201),  -- ����� �� 201 � ������� ���������
			BuildDate,
			RetireDate,
			EndDate,
			AirCraftLineNumber_LN_MSN,
			TRY_CAST(TRY_CAST(AirCraftLineNumber_LN_MSN AS FLOAT) AS BIGINT),  -- ������������� � BIGINT, ������� 'nan' � ��� ��������� �� ������ ������
			AirCraftSerialNumber_SN,  -- � �������� ������ �����, ����� � �����������
			AirCraftCNumber,
			TRY_CAST(TRY_CAST(AirCraftCNumber AS FLOAT) AS BIGINT),
			SourceCSVFile,
			AirCraftDescription
			FROM [data-server-1.movistar.vrn.skylink.local].AirFlightsDBNew62WorkBase.dbo.AirCraftsTable
-- COMMIT TRANSACTION

-- ������ ������� ����� ��������� ������� (��� �������� ������������ ������� �� ���������) - �� �������

/*
SELECT	AirCraftRegistration,  -- ������������� � XML-��� ���� �� ����� ������������� �������
		(AirCraftModel + 201),  -- ����� �� 201 � ������� ���������
		BuildDate,  -- ���� ��������� ��� ������
		RetireDate,  -- ���� ��������� ��� ������
		SourceCSVFile,
		AirCraftDescription,
		AirCraftLineNumber_LN_MSN,  -- ���� ��������� ��� ������, �������������� � BIGINT, �������� 'nan' � ��� ��������� �� ������ ������ -> ������
		AirCraftLineNumber_LN_NEW AS TRY_CAST(TRY_CAST(AirCraftLineNumber_LN_MSN AS FLOAT) AS BIGINT),  -- ���� ��������� ��� ������, �������������� � BIGINT, �������� 'nan' � ��� ��������� �� ������ ������ -> ������
		AirCraftSerialNumber_SN,  -- ���� ��������� ��� ������
		AirCraftCNumber,
		-- TRY_CONVERT(BIGINT, AirCraftCNumber),  -- ���� ��������� ��� ������, �������������� � BIGINT, �������� 'nan' � ��� ��������� �� ������ ������ -> ������
		EndDate  -- ���� ��������� ��� ������
	INTO  ##AirCraftsTableNew2XsdIntermediate  -- �� ��������� ������� (�������� ��� ������ ��������)
		FROM [data-server-1.movistar.vrn.skylink.local].AirFlightsDBNew62WorkBase.dbo.AirCraftsTable

SELECT * FROM ##AirCraftsTableNew2XsdIntermediate
*/
