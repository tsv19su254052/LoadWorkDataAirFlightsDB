USE [AirLinesDBNew62]
GO

/****** Object:  XmlSchemaCollection [dbo].[SchemaHubs_Simple]    Script Date: 23.02.2023 3:07:25 am ******/
CREATE XML SCHEMA COLLECTION [dbo].[SchemaHubs_Simple] AS N'
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
			xmlns:t="https://www.w3schools.com" 
			targetNamespace="https://www.w3schools.com" 
			elementFormDefault="qualified">
			
			<xsd:element name="AirLine_Codes">
				<xsd:complexType>
					<xsd:complexContent>
						<xsd:restriction base="xsd:anyType">
							<xsd:sequence>
								<xsd:element name="Hub" maxOccurs="unbounded">
									<xsd:complexType>
										<xsd:complexContent>
											<xsd:restriction base="xsd:anyType">
												<xsd:sequence>
													<xsd:element name="AirPort_FK_IATA">
														<xsd:complexType>
															<xsd:simpleContent>
																<xsd:extension base="xsd:token">
																	<xsd:attribute name="enabled" type="xsd:boolean" use="required" />
																</xsd:extension>
															</xsd:simpleContent>
														</xsd:complexType>
													</xsd:element>
                                                    <xsd:element name="AirPort_FK_ICAO">
                                                        <xsd:complexType>
															<xsd:simpleContent>
																<xsd:extension base="xsd:token">
																	<xsd:attribute name="enabled" type="xsd:boolean" use="required" />
																</xsd:extension>
															</xsd:simpleContent>
														</xsd:complexType>
													</xsd:element>
												</xsd:sequence>
											</xsd:restriction>
										</xsd:complexContent>
									</xsd:complexType>
								</xsd:element>
							</xsd:sequence>
						</xsd:restriction>
					</xsd:complexContent>
				</xsd:complexType>
			</xsd:element>
</xsd:schema>'
GO


