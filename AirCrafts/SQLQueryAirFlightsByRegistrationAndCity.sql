-- Перелеты по регистрации самолета с аэропортами
DECLARE @City VARCHAR(250), @Reg VARCHAR(50)
SET @Reg = 'N67158'  -- 27144
SET @City = 'Denver'  -- 148
-- SET STATISTICS XML ON

SET Transaction Isolation Level Read Committed
SELECT		AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByFlightDate.FlightDate AS FLIGHTDATE,
			AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByFlightDate.FlightNumberString AS FNS,
			AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortName AS DEPARTURE,
			AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortCity AS CITY_OUT,
			AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortCodeIATA AS IATA_OUT,
			AirPortsTable_1.AirPortName AS ARRIVAL,
			AirPortsTable_1.AirPortCity AS CITY_IN,
			AirPortsTable_1.AirPortCodeIATA AS IATA_IN,
			AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByFlightDate.QuantityCounted
	FROM	AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByFlightDate
			INNER JOIN AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate ON AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByFlightDate.AirCraft = AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate.AirCraftUniqueNumber 
			INNER JOIN AirPortsAndRoutesDBNew62.dbo.AirRoutesTable ON AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByFlightDate.AirRoute = AirPortsAndRoutesDBNew62.dbo.AirRoutesTable.AirRouteUniqueNumber 
			INNER JOIN AirPortsAndRoutesDBNew62.dbo.AirPortsTable ON AirPortsAndRoutesDBNew62.dbo.AirRoutesTable.AirPortDeparture = AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortUniqueNumber 
			INNER JOIN AirPortsAndRoutesDBNew62.dbo.AirPortsTable AS AirPortsTable_1 ON AirPortsAndRoutesDBNew62.dbo.AirRoutesTable.AirPortArrival = AirPortsTable_1.AirPortUniqueNumber  
		WHERE AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate.AirCraftRegistration = @Reg
/*
Вывод:
большие самолеты American AirLines, Continental как правило более привязаны к маршруту
	UTair Boeing 767-224(ER):
		VP-BAG UTair Aviation 15.07.2012 Moscow - Dushanbe, Tashkent, Makhachkala - Jeddah, Anadyr		(N76156 Continental Airlines 15.02.2001 -> United Airlines 01.12.2011) 95 строк
		VP-BAI UTair Aviation 02.09.2012 Moscow - Dushanbe, Tashkent ,Bukhara, Anadyr					(N67158 Continental Airlines 30.05.2001 -> United Airlines 01.12.2011) 97 строк
		VP-BAL UTair Aviation 21.07.2014 Moscow - Dushanbe, Tashkent ,Bukhara							(N68160 Continental Airlines 30.10.2001 -> United Airlines 01.12.2011) 157 строк
	New York City 11.09.2001
		N334AA - 11.09.2001 New York City 92(i)+1600 crashed into WTC Northern tower 8:45 am after hyjack ER Boston - Los Angeles flight #11, tt 58350, 11538 l, most died at collapse of tower at 10:29 am, own NEMLC 8.07.87, FUNB r6.01.00 118 строк
		N612UA - 11.09.2001 New York City 65(i)+1000 crashed into WTC Southern tower 9:03 am after hyjack ER Boston - Los Angeles flight #175, tt 66647, 17549 l, most occ. killed when tower collapsed at 09:50 am 179 строк
*/
			ORDER BY FLIGHTDATE, FNS, CITY_OUT, CITY_IN  -- 27144

SELECT		AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortName AS DEPARTURE,
			AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortCity AS CITY_OUT,
			AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortCodeIATA AS IATA_OUT,
			AirPortsTable_1.AirPortName AS ARRIVAL,
			AirPortsTable_1.AirPortCity AS CITY_IN,
			AirPortsTable_1.AirPortCodeIATA AS IATA_IN,
			SUM(AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByFlightDate.QuantityCounted) AS QUANTITY
	FROM	AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByFlightDate 
			INNER JOIN AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate ON AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByFlightDate.AirCraft = AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate.AirCraftUniqueNumber 
			INNER JOIN AirPortsAndRoutesDBNew62.dbo.AirRoutesTable ON AirCraftsDBNew62.dbo.AirFlightsTableIntermediateByFlightDate.AirRoute = AirPortsAndRoutesDBNew62.dbo.AirRoutesTable.AirRouteUniqueNumber 
			INNER JOIN AirPortsAndRoutesDBNew62.dbo.AirPortsTable ON AirPortsAndRoutesDBNew62.dbo.AirRoutesTable.AirPortDeparture = AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortUniqueNumber 
			INNER JOIN AirPortsAndRoutesDBNew62.dbo.AirPortsTable AS AirPortsTable_1 ON AirPortsAndRoutesDBNew62.dbo.AirRoutesTable.AirPortArrival = AirPortsTable_1.AirPortUniqueNumber  
		WHERE AirCraftRegistration = @Reg
			GROUP BY	AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortName,
						AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortCity,
						AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortCodeIATA,
						AirPortsTable_1.AirPortName,
						AirPortsTable_1.AirPortCity,
						AirPortsTable_1.AirPortCodeIATA
			ORDER BY CITY_OUT, CITY_IN
