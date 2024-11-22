USE AirCraftsDBNew62
GO

SET STATISTICS XML ON
SET STATISTICS IO ON
SET STATISTICS TIME ON
SET STATISTICS PROFILE ON

DECLARE @Reg VARCHAR(50), @FNS VARCHAR(100), @Route BIGINT, @FD DATE, @BD DATE, @Quantity BIGINT, @Result INT, @ReturnValue INT, @xml XML
SET @Reg = 'N000AA'  -- �� ������
SET @FNS = '9E5028Test'  -- ���� 9E5028
SET @Route = 87  -- ���� 87
SET @FD = '2023-08-21'  -- ���� 2023-09-21
SET @BD = '2023-08-01'  -- ���� 2023-09-01
SET @Quantity = 1

SET Transaction Isolation Level Repeatable Read
BEGIN TRANSACTION
IF (SELECT FlightsByRoutes FROM AirCraftsTableNew2XsdIntermediate WITH (UPDLOCK) WHERE AirCraftRegistration = @Reg) IS NULL
	BEGIN
		-- ���� XML-��� ���� ��� ������
		PRINT '���������� � ���� ����� ���� ' + CONVERT(VARCHAR(100), @FNS) + ', ������� ' + CONVERT(VARCHAR(100), @Route) + ' � ����������� ' + CONVERT(VARCHAR(100), @FD)
		SET @xml = '<FlightsByRoutes>
						<Flight FlightNumberString="' + CONVERT(VARCHAR(5000), @FNS) + '">
							<Route RouteFK="' + CONVERT(VARCHAR(5000), @Route) + '">
								<step FlightDate="' + CONVERT(VARCHAR(5000), @FD) + '" BeginDate="' + CONVERT(VARCHAR(5000), @BD) + '">
									1
								</step>
							</Route>
						</Flight>
					</FlightsByRoutes>'
		-- PRINT ' ++ xml ��� ����� ������ = ' + CONVERT(VARCHAR(5000), @xml)
		UPDATE AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes = @xml WHERE AirCraftRegistration = @Reg
		SET @Result = 3
	END
ELSE
	BEGIN
		IF (SELECT FlightsByRoutes.exist('/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]') 
			FROM  AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = @Reg) = 1
			BEGIN
				IF (SELECT FlightsByRoutes.exist('/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")]') 
					FROM AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = @Reg) = 1
					BEGIN
						IF (SELECT FlightsByRoutes.exist('/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")]/step[@FlightDate=sql:variable("@FD")]') 
							FROM AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = @Reg) = 1
								BEGIN
									PRINT '� ����� ' + CONVERT(VARCHAR(100), @FNS) + ' � � �������� ' + CONVERT(VARCHAR(100), @Route) + ' ������� ����������� ' + CONVERT(VARCHAR(100), @FD)
									SET @Quantity = (SELECT FlightsByRoutes.value(('(/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")]/step[@FlightDate=sql:variable("@FD")])[1]'), 'BIGINT') 
														FROM AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = @Reg)
									SET @Quantity += 1
									-- � �������� WHERE �� ��������, ��. ������ https://www.mssqltips.com/sqlservertip/2738/examples-of-using-xquery-to-update-xml-data-in-sql-server/ ������ "Modify() Limitations Issue # 1"
									-- UPDATE dbo.AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('replace value of (/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")]/step[@FlightDate=sql:variable("@FD")]/text()) with sql:variable("@Quantity") ')  WHERE AirCraftRegistration = @Reg
									-- ����� �������� ��� XML-��� ����, �� ������ � ������ ����������
									SET @xml = (SELECT FlightsByRoutes FROM AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = @Reg)
									SET @xml.modify('replace value of (/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")]/step[@FlightDate=sql:variable("@FD")]/text())[1] with sql:variable("@Quantity") ')
									UPDATE AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes = @xml WHERE AirCraftRegistration = @Reg
									PRINT ' - ������������� = ' + CONVERT(VARCHAR(100), @Quantity)
									SET @Result = 2
								END
						ELSE
							BEGIN
								PRINT '���������� � ���� ' + CONVERT(VARCHAR(100), @FNS) + ' � � ������� ' + CONVERT(VARCHAR(100), @Route) + ' ����� ����������� ' + CONVERT(VARCHAR(100), @FD)
								UPDATE AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('insert <step FlightDate="{sql:variable("@FD")}" BeginDate="{sql:variable("@BD")}">1</step> into (/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")])[1]') WHERE AirCraftRegistration = @Reg
								SET @Result = 1
							END
					END
				ELSE
					BEGIN
						PRINT '���������� � ���� ' + CONVERT(VARCHAR(100), @FNS) + ' ����� ������� ' + CONVERT(VARCHAR(100), @Route) + ' � ����������� ' + CONVERT(VARCHAR(100), @FD)
						UPDATE AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('insert <Route RouteFK="{sql:variable("@Route")}"><step FlightDate="{sql:variable("@FD")}" BeginDate="{sql:variable("@BD")}">1</step></Route> into (/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")])[1]') WHERE AirCraftRegistration = @Reg
						SET @Result = 1
					END
			END
		ELSE
			BEGIN
				PRINT '���������� ����� ���� ' + CONVERT(VARCHAR(100), @FNS) + ', ������� ' + CONVERT(VARCHAR(100), @Route) + ' � ����������� ' + CONVERT(VARCHAR(100), @FD)
				UPDATE AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('insert <Flight FlightNumberString="{sql:variable("@FNS")}"><Route RouteFK="{sql:variable("@Route")}"><step FlightDate="{sql:variable("@FD")}" BeginDate="{sql:variable("@BD")}">1</step></Route></Flight> into (/FlightsByRoutes)[1]') WHERE AirCraftRegistration = @Reg
				SET @Result = 1
			END
	END
COMMIT TRANSACTION
PRINT ' - ��������� ������� = ' + CONVERT(VARCHAR(100), @Result) + ' (���� ��������: 0 - ����������, 1 - ��������, 2 - ����������, 3 - ������ ������ � ��� ������ ������)'

PRINT '�� �� � ������� �������� ���������'
EXECUTE @ReturnValue = dbo.SPFlightInsertOrUpdate @Reg, @FNS, @Route, @FD, @BD
PRINT ' - ��������� ��������� = ' + CONVERT(VARCHAR(100), @ReturnValue) + ' (���� ��������: 0 - ����������, 1 - ��������, 2 - ����������, 3 - ������ ������ � ��� ������ ������)'

PRINT '�������'
SELECT	AirCraftRegistration,
		FlightsByRoutes.query('for $flights in /FlightsByRoutes/Flight where $flights/Route/step/@BeginDate = sql:variable("@BD") return $flights') AS FlightsAfter
	FROM AirCraftsTableNew2XsdIntermediate
		INNER JOIN AirCraftModelsTable ON AirCraftsTableNew2XsdIntermediate.AirCraftModel = AirCraftModelsTable.AirCraftModelUniqueNumber
		INNER JOIN AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
		WHERE FlightsByRoutes.exist('/FlightsByRoutes/Flight/Route/step[@BeginDate = sql:variable("@BD")]') = 1 AND AirCraftRegistration = @Reg
		-- WHERE AirCraftRegistration = @Reg
			ORDER BY AirCraftRegistration

-- fixme �������� �������� (������ ���� ������), XSD-����� �������� -> �������� ��������
UPDATE AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('delete /FlightsByRoutes/Flight[@FlightNumberString = sql:variable("@FNS")]') WHERE AirCraftRegistration = @Reg
PRINT '������� ������� �� ' + CONVERT(VARCHAR(100), @FD)

PRINT '���������'
SELECT	AirCraftRegistration,
		FlightsByRoutes.query('for $flights in /FlightsByRoutes/Flight where $flights/Route/step/@BeginDate = sql:variable("@BD") return $flights') AS FlightsBefore
	FROM AirCraftsTableNew2XsdIntermediate
		INNER JOIN AirCraftModelsTable ON AirCraftsTableNew2XsdIntermediate.AirCraftModel = AirCraftModelsTable.AirCraftModelUniqueNumber
		INNER JOIN AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
		WHERE FlightsByRoutes.exist('/FlightsByRoutes/Flight/Route/step[@BeginDate = sql:variable("@BD")]') = 1 AND AirCraftRegistration = @Reg
		-- WHERE AirCraftRegistration = @Reg
			ORDER BY AirCraftRegistration
