USE AirLinesDBNew62
GO

-- В кавычках вставить содержимое схемы из файла *.xsd
CREATE XML SCHEMA COLLECTION SchemaHREFs_Simple AS '
<!-- Начало вставки сводной XSD-схемы -->

<!-- Вверху сводный перечень пространств имен, todo Дополнить шапку из сгенерированной XSD-схемы -->
<xs:schema  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
			xmlns:xs="http://www.w3.org/2001/XMLSchema"
			xmlns:ns="https://www.w3schools.com"
			xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
			xmlns:xml="http://www.w3.org/XML/1998/namespace"
			xmlns:fn="http://www.w3.org/2004/07/xpath-functions"
			xmlns:xdt="http://www.w3.org/2004/07/xpath-datatypes"
			xmlns:xlink="http://www.w3.org/1999/xlink"
			xmlns:xi="http://www.w3.org/2001/XInclude"
			xmlns:css="http://www.w3.org/1996/css"
			xmlns:collation="http://www.w3.org/2013/collation/UCA?strength=secondary"
			xmlns:xsv="http://www.w3.org/2007/XMLSchema-versioning"
			xmlns:xproc="http://www.w3.org/ns/xproc"
			xmlns:xproc-step="http://www.w3.org/ns/xproc-step"
			xmlns:err="http://www.w3.org/ns/xproc-error"
			xmlns:xhtml="http://www.w3.org/1999/xhtml"
			xmlns:sqltypes="https://schemas.microsoft.com/sqlserver/2004/sqltypes"
			xmlns:soap="https://schemas.microsoft.com/sqlserver/2004/SOAP"
			xmlns:ms="urn:schemas-microsoft-com:mapping-schema"
			xmlns:dt="urn:schemas-microsoft-com:datatypes"
			xmlns:sql="urn:schemas-microsoft-com:xml-sql"
			xmlns:soapex="http://schemas.xmlsoap.org/soap/envelope"
			xmlns:saxon="http://saxon.sf.net"
			xmlns:schematron="http://purl.oclc.org/dsdl/schematron"
			xmlns:set="http://transpect.io/xml2tex"
			xmlns:tr="http://transpect.io"
			xmlns:pxf="http://exproc.org/proposed/steps/file"
			xmlns:rng="http://relaxng.org/ns/structure/1.0"
			xmlns:rnga="http://relaxng.org/ns/compatibility/annotations/1.0"
			
			attributeFormDefault="unqualified" 
			elementFormDefault="qualified" 
			targetNamespace="https://www.w3schools.com">

	<xs:annotation>
		<xs:documentation>
			Сводная схема по ссылкам
		</xs:documentation>
	</xs:annotation>

	<!-- todo Вставить элементы из сгенерированных XSD-схем -->
	<!-- Начало вставки -->

	<xs:element name="AirLine_HREFs">
		<xs:complexType>
			<xs:sequence>
				<xs:element name="hrefToWikiPedia">
					<xs:complexType>
						<xs:simpleContent>
							<xs:extension base="xs:string">
								<xs:attribute name="site" type="xs:anyURI" use="required" />
							</xs:extension>
						</xs:simpleContent>
					</xs:complexType>
				</xs:element>
				<xs:element name="hrefToSite">
					<xs:complexType>
						<xs:simpleContent>
							<xs:extension base="xs:string">
								<xs:attribute name="site" type="xs:anyURI" use="required" />
							</xs:extension>
						</xs:simpleContent>
					</xs:complexType>
				</xs:element>
			</xs:sequence>
		</xs:complexType>
	</xs:element>

	<!-- Окончание вставки -->

</xs:schema>

<!-- Окончание вставки сводной XSD-схемы -->
'

PRINT 'Привязал сводную XSD-схему к базе в коллекцию dbo.SchemaHREFs_Simple'
GO
