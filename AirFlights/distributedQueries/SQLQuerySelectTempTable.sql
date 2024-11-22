-- :CONNECT data-server-1.movistar.vrn.skylink.local
:CONNECT terminalserver\sqldeveloper
USE tempdb
GO

SELECT * FROM ##AirFlightsCraftsTempTable
-- SELECT * FROM dbo.#BAB45CF7  -- выдает ошибку Недопустимое имя объекта
