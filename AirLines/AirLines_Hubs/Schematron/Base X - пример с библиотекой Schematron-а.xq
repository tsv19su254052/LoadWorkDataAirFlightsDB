xquery version "3.1" encoding "utf-8";

(:~ 
  Как искать и подветкам в XML-ном файле элемент с указанным значением? Как вставить новую подветку, если элемент не найдено? Как добавить еще одну подветку, если элемент найден?
  Как искать и подветкам в XML-ном файле аттрибут с указанным значением? Как изменить значение найденного аттрибута?
 :)

import module namespace schematron = "http://github.com/Schematron/schematron-basex";

declare namespace expath = "http://expath.org/ns/pkg";
declare namespace svrl = "http://purl.oclc.org/dsdl/svrl";
declare namespace sch = "http://purl.oclc.org/dsdl/schematron";
declare namespace xsl = "http://www.w3.org/1999/XSL/Transform";

(: ---- Модуль не найден ----
import module namespace schxslt = "https://doi.org/10.5281/zenodo.1495494";

declare %private function schxslt:processor-path ($queryBinding as xs:string) as xs:string {
  switch ($queryBinding)
    case ""
      return "1.0"
    case "xslt"
      return "1.0"
    case "xslt2"
      return "2.0"
    case "xslt3"
      return "2.0"
    default
      return error(xs:QName("schxslt:UnsupportedQueryBinding"))
};

declare function schxslt:compile ($schematron as node(), $options as map(*), $xsltver as xs:string) as document-node(element(xsl:transform)) {
  let $basedir := file:base-dir() || "/xslt/" || $xsltver || "/"
  let $include := $basedir || "include.xsl"
  let $expand  := $basedir || "expand.xsl"
  let $compile := $basedir || "compile-for-svrl.xsl"
  return
    $schematron => xslt:transform($include) => xslt:transform($expand) => xslt:transform($compile, $options)
};

:)

(:
import module namespace util = "util" at "util-lib.xqy";
import module namespace process = "process" at "process-lib.xqy";
import module namespace query = "query" at "query-lib.xqy";
:)

(:
import module namespace Cast = "bib_cast" at "file:C:\GregTemp\CompteurCRO\saxon.net\gregtest\bib_cast.xquery";
import module namespace Casti = "bib_casti" at "file:C:\GregTemp\CompteurCRO\saxon.net\gregtest\bib_casti.xquery";
:)

(:~
 : Validate document against Schematron and return the validation report.
 :
 : @param  $document   Document to be validated
 : @param  $schematron Schematron schema
 : @param  $phase      Validation phase
 : @return Validation report
 
 : Compile Schematron to validation stylesheet.
 :
 : @param  $schematron Schematron document
 : @param  $options Schematron compiler parameters
 : @return Validation stylesheet
:)

let $a := 2
let $b := trace(4, "text")
let $c := 5

(:console:log($b as xs:integer) - выдает ошибку :)

return (
  (:<result><return>{$d}</return></result>:)
  $a, $b, $c
)
