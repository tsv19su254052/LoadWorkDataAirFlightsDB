USE AirCraftsDBNew62
GO

-- в кавычках вставить содержимое схемы из файла *.xsd
CREATE XML SCHEMA COLLECTION SchemaFlightsByRoutesUnbounded AS '
<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema">
	<xs:element name="FlightsByRoutes">
		<xs:complexType>
			<xs:sequence>
				<xs:element maxOccurs="unbounded" name="Flight">
					<xs:complexType>
						<xs:sequence>
							<xs:element maxOccurs="unbounded" name="Route">
								<xs:complexType mixed="true">
									<xs:sequence minOccurs="0">
										<xs:element maxOccurs="unbounded" name="step">
											<xs:complexType>
												<xs:simpleContent>
													<xs:extension base="xs:unsignedLong">
														<xs:attribute name="FlightDate" type="xs:date" use="required" />
														<xs:attribute name="BeginDate" type="xs:date" use="required" />
													</xs:extension>
												</xs:simpleContent>
											</xs:complexType>
										</xs:element>
									</xs:sequence>
									<xs:attribute name="RouteFK" type="xs:unsignedLong" use="required" />
								</xs:complexType>
							</xs:element>
						</xs:sequence>
						<xs:attribute name="FlightNumberString" type="xs:string" use="required" />
					</xs:complexType>
				</xs:element>
			</xs:sequence>
		</xs:complexType>
	</xs:element>

	<!-- Старая часть схемы (с ошибками)
	<xs:element name="FlightsByRoutes">
		<xs:complexType>
			<xs:sequence>
				<xs:element maxOccurs="unbounded" name="Flight">
					<xs:complexType>
						<xs:sequence>
							<xs:element maxOccurs="unbounded" name="Route">
								<xs:complexType>
									<xs:sequence>
										<xs:element maxOccurs="unbounded" name="step">
											<xs:complexType>
												<xs:simpleContent>
													<xs:extension base="xs:unsignedByte">
														<xs:attribute name="FlightDate" type="xs:date" use="required" />
														<xs:attribute name="BeginDate" type="xs:date" use="required" />
													</xs:extension>
												</xs:simpleContent>
											</xs:complexType>
										</xs:element>
									</xs:sequence>
									<xs:attribute name="RouteFK" type="xs:unsignedLong" use="required" />
								</xs:complexType>
							</xs:element>
						</xs:sequence>
						<xs:attribute name="FlightNumberString" type="xs:string" use="required" />
					</xs:complexType>
				</xs:element>
			</xs:sequence>
		</xs:complexType>
	</xs:element>
	-->
</xs:schema>'

PRINT 'Создана коллекция схем XSD - dbo.SchemaFlightsByRoutesUnbounded'
GO
