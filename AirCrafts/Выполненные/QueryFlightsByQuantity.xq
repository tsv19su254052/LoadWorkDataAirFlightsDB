let $date := "1997-08-01"
for $steps in /FlightsByRoutes/Flight/Route/step
where $steps=2
return $steps
