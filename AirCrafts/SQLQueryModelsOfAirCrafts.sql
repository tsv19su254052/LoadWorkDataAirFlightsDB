USE AirCraftsDBNew62
GO

SELECT	AirCraftModelUniqueNumber,
		ModelName,
		ModelNumber,
		ManufacturerName,
		ManufacturerDescription,
		ModelDescription
	FROM	AirCraftModelsTable
			INNER JOIN AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
ORDER BY ManufacturerName, ModelName