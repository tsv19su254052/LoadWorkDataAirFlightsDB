let $date := "1998-07-01"
for $steps in /FlightsByRoutes/Flight/Route/step
where $steps/@BeginDate=$date
return $steps
