let $faildate := "1996-05-01"
for $steps in /FlightsByRoutes/Flight/Route/step
where $steps/@BeginDate=$faildate
return (delete nodes /FlightsByRoutes/Flight/Route/step[@BeginDate = $faildate])

(:
for $steps in /FlightsByRoutes/Flight/Route/step
where $steps/@BeginDate=$faildate
return $steps
:)
