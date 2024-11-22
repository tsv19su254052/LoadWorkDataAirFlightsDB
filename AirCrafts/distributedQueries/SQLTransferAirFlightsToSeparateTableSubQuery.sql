SELECT TOP 1 AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate.AirCraftUniqueNumber
			FROM	AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate
					INNER JOIN AirFlightsDBNew72WorkBase.dbo.AirCraftsTable ON AirCraftsTable.AirCraftRegistration = AirCraftsTableNew2XsdIntermediate.AirCraftRegistration
					INNER JOIN AirFlightsDBNew72WorkBase.dbo.AirFlightsTable ON AirFlightsTable.AirCraft = AirCraftsTable.AirCraftUniqueNumber
						WHERE AirFlightsDBNew72WorkBase.dbo.AirFlightsTable.AirCraft = 4

SELECT AirCraftUniqueNumber 
	FROM AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate 
		WHERE AirCraftRegistration = (SELECT AirCraftRegistration FROM AirFlightsDBNew72WorkBase.dbo.AirCraftsTable 
										WHERE AirCraftUniqueNumber = (SELECT TOP 1 AirCraft FROM AirFlightsDBNew72WorkBase.dbo.AirFlightsTable WHERE FlightNumberString = 'AA1'))

SELECT AirCraftUniqueNumber 
	FROM AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate 
		WHERE AirCraftRegistration = (SELECT AirCraftRegistration FROM AirFlightsDBNew72WorkBase.dbo.AirCraftsTable 
											WHERE AirCraftUniqueNumber = 201)
