-- ��������� ��� �������� ���������
USE AirPortsAndRoutesDBNew62
GO

DECLARE @iata NVARCHAR(10), @icao NVARCHAR(10), @User NVARCHAR(100), @Host NVARCHAR(100), @DateTime DATETIME
SET @iata = 'LAX'
SET @icao = 'KLAX'
SET @User = 'Andrey'
SET @Host = 'TerminalServer3'
SET @DateTime = GETDATE()


BEGIN TRANSACTION updateLogCountViewed WITH MARK  -- ������� ���������� (�������� � SQL Server 2008-��)
-- ����� ������ � ������ ��� SAX - ����� � ��������� (DOM - ������ XML-��� ���� � XML-��� ����������, ������ �� � ����� �������)
SET Transaction Isolation Level Repeatable Read
IF @iata IS NOT NULL AND @icao IS NOT NULL
	BEGIN
		PRINT 'IATA � ICAO'
		IF (SELECT LogDateAndTimeViewed FROM dbo.AirPortsTable WHERE AirPortCodeIATA = @iata AND AirPortCodeICAO = @icao) IS NULL
			BEGIN
				PRINT '��������� ��� � ����'
				UPDATE dbo.AirPortsTable SET LogDateAndTimeViewed = '<Viewed> <User Name = "{ sql:variable("@User") }"> <DateTime From = "{ sql:variable("@Host") }"> sql:variable("@DateTime") </DateTime> </User> </Viewed> ' 
					WHERE AirPortCodeIATA = @iata AND AirPortCodeICAO = @icao
			END
		ELSE
			BEGIN
				IF (SELECT LogDateAndTimeViewed.exist('/Viewed/User = "{ sql:variable("@User") }" ') FROM dbo.AirPortsTable WHERE AirPortCodeIATA = @iata AND AirPortCodeICAO = @icao) = 0
					BEGIN
						PRINT '��������� ����� �������� � �������� ������� � � Host-��'
						UPDATE dbo.AirPortsTable SET LogDateAndTimeViewed.modify('insert <DateTime From = "{ sql:variable(@Host) }"> "{ sql:variable(@DateTime) }" </DateTime> into /Viewed/User = "{ sql:variable(@User) }" ')
							WHERE AirPortCodeIATA = @iata AND AirPortCodeICAO = @icao
					END
				ELSE
					BEGIN
						PRINT '��������� ����� �������� � ����� User-�� � � �������� ������� � Host-��'
						UPDATE dbo.AirPortsTable SET LogDateAndTimeViewed.modify('insert <User Name = "{ sql:variable(@User) }"> <DateTime From = "{ sql:variable(@Host) }"> "{ sql:variable(@DateTime) }" </DateTime> </User> into /Viewed ')
							WHERE AirPortCodeIATA = @iata AND AirPortCodeICAO = @icao
					END
			END
	END
ELSE
	BEGIN
		IF @iata IS NULL AND @icao IS NULL
			BEGIN
				PRINT ' - and -'
			END
		ELSE
			BEGIN
				IF @iata IS NULL
					BEGIN
						PRINT ' - and ICAO'
					END
				IF @icao IS NULL
					BEGIN
						PRINT ' IATA and -'
					END
			END
	END
COMMIT TRANSACTION

