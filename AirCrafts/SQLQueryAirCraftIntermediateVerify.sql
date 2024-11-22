SET Transaction Isolation Level Read Committed

/*
-- ���������, ��� ��������� ��������
SELECT * 
	FROM AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate
		-- WHERE AirCraftSerialNumber_SN_OLD IS NOT NULL  -- � ���� ������ SN
			ORDER BY AirCraftRegistrationOld, AirCraftModel  -- 84691
*/

SELECT COUNT(*) AS CountTotal
	FROM AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate  -- 84691 -> 84781

-- � ���� ���������:
--  - � ������� ��������� "AirCraftsTableNew2Xsd" ��������� � ������� �������� � ������� ������ ��������� � �� �������� (����� ���������� �� �� ������ � ������ ��� ����� ����) -> �������.
--  - ����������� �������� (����. Tail Number) � �������� ������� ����� ��������������� ��������� ��� ���������� �� ������ �������� � �������.
--  - ������� �� ����� ������������ ����� ��������� ��� �������� ���� ��������������� �����.
--  - ������� ���������� ������������ ���������� ��� ��������� ������� `LN`, `MSN`, `SN`, `CN` � ����������� �� �����-������������.
-- � ���� �������������:
--  - � ���� ������������� �������� ������ ��� ����, ��� ������� � ������������ �������� ������� � ��������� ����, �� ��������� ����� �� �������� ��������.
--  - ������������ ����������� �������� �� ����� �������� � ������ ��� ������.

-- UPDATE AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes = NULL

SELECT	AirCraftRegistration,
		FlightsByRoutes,
		BuildDate,
		RetireDate,
		EndDate,
		AirCraftLineNumber_LN_OLD AS LN_OLD,
		AirCraftLineNumber_LN_NEW AS LN_NEW,
		AirCraftLineNumber_MSN AS MSN,
		AirCraftSerialNumber_SN AS SN,
		AirCraftCNumber_CN_OLD AS CN_OLD,
		AirCraftCNumber_CN_NEW AS CN_NEW,
		-- AirCraftModel,
		ManufacturerName,
		ModelName,
		SourceCSVFile,
		AirCraftDescription
	FROM AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate
		INNER JOIN AirCraftsDBNew62.dbo.AirCraftModelsTable ON AirCraftsTableNew2XsdIntermediate.AirCraftModel = AirCraftModelsTable.AirCraftModelUniqueNumber
		INNER JOIN AirCraftsDBNew62.dbo.AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
		WHERE ModelName = 'DC-10'
		-- WHERE FlightsByRoutes IS NOT NULL  -- AND AirCraftRegistration = 'nan'
		-- WHERE FlightsByRoutes.value(('/FlightsByRoutes/Flight/Route/step/@BeginDate'), 'DATE') = '1995-01-01'  -- VARCHAR(50)
			ORDER BY AirCraftRegistration

/*
SELECT	AirCraftRegistrationOld,
		BuildDate,
		RetireDate,
		EndDate,
		AirCraftSerialNumber_SN,
		AirCraftCNumber,
		ManufacturerName,
		ModelName,
		SourceCSVFile
	FROM	AirCraftsDBNew62.dbo.AirCraftManufacturersTable
			INNER JOIN AirCraftsDBNew62.dbo.AirCraftModelsTable ON AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber = AirCraftModelsTable.Manufacturer 
			CROSS JOIN AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate
		ORDER BY AirCraftRegistrationOld, ModelName  -- ���������� 17107582 ����� (�������� �� 202 - ���������� �������)!!!!

SELECT	AirCraftRegistrationOld,
		BuildDate,
		RetireDate,
		EndDate,
		AirCraftSerialNumber_SN,
		AirCraftCNumber,
		ManufacturerName,
		ModelName,
		SourceCSVFile
	FROM	AirCraftsDBNew62.dbo.AirCraftManufacturersTable
			INNER JOIN AirCraftsDBNew62.dbo.AirCraftModelsTable ON AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber = AirCraftModelsTable.Manufacturer 
			CROSS APPLY AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate
		ORDER BY AirCraftRegistrationOld, ModelName  -- ���������� 17107582 ����� (�������� �� 202 - ���������� �������)!!!!
*/
