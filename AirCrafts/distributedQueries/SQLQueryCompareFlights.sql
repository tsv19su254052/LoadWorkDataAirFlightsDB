-- Сравниваем перелеты в таблице перелетов и в таблице регистраций
DECLARE @reg VARCHAR(50)
DECLARE @begindate DATE, @enddate DATE, @currentdate DATE
SET @begindate = '1997-11-01'
SET @enddate = '1997-12-01'

