SELECT * 
  FROM [AirLinesDBNew62].[dbo].[AirLinesTable]
  -- WHERE AirLineCodeIATA IS NULL AND AirLineCodeICAO = 'None'
  WHERE AirLineCodeIATA IS NULL AND AirLineCodeICAO IS NULL
  GO

  -- UPDATE [AirLinesDBNew62].[dbo].[AirLinesTable] SET  AirLineCodeIATA = 'VC', AirLineCodeICAO = 'CIG' WHERE  AirLineCodeIATA IS NULL AND AirLineCodeICAO = 'None'
  GO
