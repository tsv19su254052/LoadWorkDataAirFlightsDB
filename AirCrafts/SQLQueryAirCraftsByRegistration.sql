USE AirCraftsDBNew62
GO

DECLARE @Reg VARCHAR(50)
SET @Reg = 'CS-TFS'
SET Transaction Isolation Level Read Committed
SELECT * 
  FROM [AirCraftsDBNew62].[dbo].[AirCraftsTableNew2Xsd]
	WHERE AirCraftRegistration.exist('/CustReg/step[@CraftRegFK=sql:variable("@Reg")]') = 1
