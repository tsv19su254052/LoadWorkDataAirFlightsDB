-- :CONNECT terminalserver\mssqlserver15
USE AirCraftsDBNew62
GO

-- ���� ������ � ������������
SET STATISTICS XML ON
SET STATISTICS IO ON
SET STATISTICS TIME ON
SET STATISTICS PROFILE ON

DECLARE @s DATE
SET @s = GETDATE()
DECLARE @Registration VARCHAR(50)  -- �����������
DECLARE @NodeNumberWithRegistration BIGINT  -- ����� �������� � ������������
DECLARE @BeginDatesTable TABLE (IDDate INT IDENTITY, BeginDateXML XML)  -- ����������-������� � �������������
DECLARE @BeginDatesNodesXML XML

SET @Registration = 'CS-TFS'

-- ����� �������� "step ... " � ���������� �������� �����������
SET Transaction Isolation Level Read Committed
BEGIN TRY
	SET @NodeNumberWithRegistration =
		(SELECT AirCraftRegistration.query('declare namespace functx ="http://functx.com";
											(:declare function functx:index-of-node ( $nodes as node()* , $nodeToFind as node() )  as xs:integer* {
												for $seq in (1 to count($nodes))
												return $seq[$nodes[$seq] is $nodeToFind]
											} ;:)
											let $nodeposition := functx:index-of-node(//step, //step[@CraftRegFK = sql:variable("@Registration")])
											return $nodeposition') AS NodePosition  -- The XQuery syntax 'declare function' is not supported - ���� �������� � ���� ������� *.xq.
			FROM AirCraftsTableNew2Xsd)  --  There is no function '{http://www.w3.org/2004/07/xpath-functions}:index-of-node()'
	-- SELECT AirCraftRegistration.query('functx:index-of(//step, //step[@CraftRegFK = sql:variable("@Registration")])') AS NodePosition FROM AirCraftsTableNew2Xsd  --  There is no function '{http://www.w3.org/2004/07/xpath-functions}:index-of()'
	-- SELECT AirCraftRegistration.query('for $Steps in //step/*[position()] where $Steps/@CraftRegFK = sql:variable("@Registration") return $Steps/BeginDate') AS NodePosition FROM AirCraftsTableNew2Xsd  -- There is no attribute named '@CraftRegFK' in the type 'element(BeginDate,xs:date)'
END TRY
BEGIN CATCH
	SET @NodeNumberWithRegistration = 125
	PRINT ' � �������� "index-of-node()" ���� �� ����������'
END CATCH
SELECT @NodeNumberWithRegistration AS NodePosition  -- ���������

;WITH XMLNAMESPACES (
	'https://www.w3schools.com' AS ns,
	'http://www.w3.org/2001/XMLSchema' AS xs,
	'http://www.w3.org/2001/XMLSchema-instance' AS xsi,
	'http://www.w3.org/2004/07/xpath-functions' AS fn,
	-- 'http://functx.com' AS functx,
	'http://www.w3.org/2005/xpath-functions' AS fnnew,
	'http://www.w3.org/2005/xpath-functions/map' AS fnmap,
	'http://www.w3.org/2005/xpath-functions/array' AS fnarray,
	'http://www.w3.org/2005/xpath-functions/math' AS fnmath,
	'http://www.w3.org/2005/xquery-local-functions' AS lfn,
	'http://libx.org/xml/libx2' AS libx,  -- �� �������
	'http://www.w3.org/1999/XSL/Transform' AS xsl,
	-- 'http://www.w3.org/XML/1998/namespace' AS nsxml,  -- XML namespace prefix 'xml' can only be associated with the URI http://www.w3.org/XML/1998/namespace. This URI cannot be used with other prefixes.
	'http://www.w3.org/2004/07/xpath-datatypes' AS xdt,
	'http://www.w3.org/1999/xlink' AS xlink,
	'http://www.w3.org/2001/XInclude' AS xi,
	'http://www.w3.org/1996/css' AS css,  -- �� �������
	'http://www.w3.org/2007/XMLSchema-versioning' AS xsv,
	'http://saxon.sf.net' AS saxon,  -- ��� ������� � ���������� �������� �� xQuery
	'http://purl.oclc.org/dsdl/schematron' AS schematron,  -- standardized by ISO/IEC FDIS 19757-3
	'http://xmlcalabash.com/ns/extensions/marklogic' AS ml)

SELECT	AirCraftRegistration.value('(/CustReg/step[@CraftRegFK = sql:variable(@Registration)]/BeginDate)[1]', 'DATE') AS BeginDate_1,
		AirCraftRegistration.value('(/CustReg/step[@CraftRegFK = sql:variable(@Registration)]/BeginDate)[2]', 'DATE') AS BeginDate_2,
		AirCraftRegistration.value('(/CustReg/step[@CraftRegFK = sql:variable(@Registration)]/BeginDate)[3]', 'DATE') AS BeginDate_3,
		AirCraftRegistration.query('for $Dates in /CustReg/step[@CraftRegFK = sql:variable(@Registration)]/BeginDate
									(: order by $Dates :)
									return data($Dates)') AS DataOfDates,
		-- AirCraftRegistration.query('for $Dates at $Position in /CustReg/step[@CraftRegFK = sql:variable("@Registration")]/BeginDate return $Position').value('.', 'BIGINT') AS NodePosition,  --  syntax 'at' is not supported
		AirCraftRegistration.query('for $Steps [at $Position] in /CustReg/step where $Steps/@CraftRegFK = sql:variable(@Registration) return <responce position="{$Position}"> {data($Steps/BeginDate)} </responce>') AS AllData,  -- syntax 'at' is not supported
		AirCraftRegistration.query('for $Steps in //step
									where $Steps/@CraftRegFK = sql:variable(@Registration)
									return data($Steps/BeginDate)') AS AllData,
		AirCraftRegistration.value('.', 'VARCHAR(5000)') AS BeginDate_all
  FROM AirCraftsTableNew2Xsd
		-- � ���������� ������� ����� ��������, �� ��������� � https://stackoverflow.com/questions/39709430/how-to-use-sql-variable-to-iterate-xml-nodes 
		WHERE AirCraftRegistration.value('(/CustReg/step/@CraftRegFK)[sql:variable(@NodeNumberWithRegistration)][1]', 'VARCHAR(50)') = @Registration

SELECT	AirCraftRegistration.value('(//step/@CraftRegFK)[sql:variable(@NodeNumberWithRegistration)][1]', 'VARCHAR(50)') AS AppropriateRegistrationV,  -- � ������ ���������� ������� ����� �������� (�������� �� ����������)
		AirCraftRegistration.value('(//step/@CraftRegFK)[2]', 'varchar(50)') AS AppropriateRegistrationC,  -- � ���������� ������� ����� �������� (�������� �������)
		-- AirCraftRegistration.value('(//step/@CraftRegFK)[position()=sql:variable("@NodeNumberWithRegistration")]', 'varchar(50)') AS AppropriateRegistrationV,  -- ������� ������
		-- AirCraftRegistration.value('let $i := sql:variable("@NodeNumberWithRegistration") (/CustReg/step/@CraftRegFK)[$i]', 'varchar(50)') AS AppropriateRegistration,  -- ������� ������
		-- AirCraftRegistration.value('/CustReg/step/@CraftRegFK/*', 'varchar(50)') AS AppropriateRegistrationAll,  -- ������� ������
		-- ���� �������� ������ ����� �����, �� �������� ����������� CROSS APPLY (��. https://stackoverflow.com/questions/23498284/why-is-cross-apply-needed-when-using-xpath-queries?noredirect=1&lq=1)
		AirCraftRegistration.query('for $Steps in /CustReg/step
									where $Steps/@CraftRegFK = sql:variable(@Registration)
									return $Steps/BeginDate') AS BeginDates,
		AirCraftRegistration.query('for $Steps in /CustReg/step
									where $Steps/@CraftRegFK = sql:variable(@Registration)
									return count($Steps/BeginDate)').value('.', 'BIGINT') AS Counts,
		AirLineOperator,  -- ��������
		AirLineOwner,  -- ��������
		AirLineLandLord,  -- ������������
		AirLineLessor  -- �������������
	FROM AirCraftsTableNew2Xsd
		WHERE AirCraftRegistration.value('(/CustReg/step/@CraftRegFK)[sql:variable(@NodeNumberWithRegistration)][1]', 'VARCHAR(50)') = @Registration  -- � ���������� ������� ����� ��������

-- todo ��������� ������������� ���� ������ ����������

BEGIN DISTRIBUTED TRANSACTION transferRegistrations
	SET Transaction Isolation Level Serializable
	INSERT INTO @BeginDatesTable (BeginDateXML)
	/*
		SELECT	AirCraftRegistration.query('for $Dates in /CustReg/step[@CraftRegFK = sql:variable("@Registration")]/BeginDate
											(: order by $Dates :)
											return $Dates').value('$Dates', 'date') AS BeginDates
	*/
		SELECT	AirCraftRegistration.query('for $Dates in /CustReg/step[@CraftRegFK = sql:variable(@Registration)]/BeginDate
											(: order by $Dates :)
											return $Dates') AS BeginDates
			FROM AirCraftsTableNew2Xsd
				-- WHERE AirCraftRegistration.value('(/CustReg/step/@CraftRegFK)[sql:variable("@NodeNumberWithRegistration")]', 'varchar(50)') = @Registration  -- ������� ������
				-- WHERE AirCraftRegistration.value('(//@CraftRegFK)[sql:variable("@NodeNumberWithRegistration")]', 'varchar(50)') = @Registration  -- ������� ������
				WHERE AirCraftRegistration.value('(/CustReg/step/@CraftRegFK)[sql:variable(@NodeNumberWithRegistration)][1]', 'VARCHAR(50)') = @Registration
		DROP TABLE IF EXISTS ##BeginDatesTempTable
		SELECT * INTO ##BeginDatesTempTable
			FROM @BeginDatesTable -- ������ ����� ��������� ������� (�������� ��� ������ ��������)
COMMIT TRANSACTION

SET Transaction Isolation Level Read Committed
SET @BeginDatesNodesXML = (SELECT TOP(1) AirCraftRegistration.query('for $Dates in /CustReg/step[@CraftRegFK = sql:variable(@Registration)]/BeginDate
																	(: order by $Dates :)
																	return $Dates')
	FROM AirCraftsTableNew2Xsd)  -- ���� ����� ���������, �� ������� ������
SELECT @BeginDatesNodesXML AS BDNX

SELECT	MyData.MD.value('(//BeginDate)[5]', 'DATE') AS BeginDateValue,
		MyData.MD.query('//BeginDate') AS BeginDateQuery,
		MyData.MD.query('//BeginDate').value('(//BeginDate)[5]', 'DATE') AS BeginDateValueInTwoSteps
	FROM @BeginDatesNodesXML.nodes('/CustReg/step/BeginDate') AS MyData(MD)
		-- WHERE AirCraftRegistration.value('(/CustReg/step/@CraftRegFK)[1]', 'varchar(50)') = @Registration
	OPTION (OPTIMIZE FOR (@BeginDatesNodesXML = NULL))  -- 2008 RTM

SELECT @@version, @@servername, DATEDIFF(s, @s, GETDATE())

SELECT * FROM ##BeginDatesTempTable
