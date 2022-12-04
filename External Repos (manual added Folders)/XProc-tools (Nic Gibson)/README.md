# XProc Tools #

## Introduction ##
This is a small set of useful XProc tools that have developed over time to provide a framework for transformation of content from one XML format to another. These are primarily used when transformation makes most sense as a sequence of transformations. 

All of these can be used via the ExPath package file or directly from the _xproc_ directory.  Each of the tools is available from  **`"http://xml.corbas.co.uk/xml/xproc-tools/"`** but use of the included *catalog.xml* file is encouraged. Note that all URLs referenced in the tools (both XProc and XSLT) use absolute URLs and will load from **xml.corbas.co.uk** unless the catalog is used.

## Namespace ##

All of these steps are in the namespace **`"http://www.corbas.co.uk/ns/xproc/steps"`** (we use the prefix `ccproc`)

## temp-dir.xpl ##

Import as  [http://xml.corbas.co.uk/xml/xproc-tools/temp-dir.xpl](http://xml.corbas.co.uk/xml/xproc-tools/temp-dir.xpl)

### ccproc:temp-dir

```xml
<p:declare-step type="ccproc:temp-dir">
  <p:output port="result"/>
  <p:option name="fallback" select="'.'"/>
</p:declare-step>
```

This step attempts to discover the system temporary directory path.  It has no inputs and a single output. The `result`  port provides a `c:result` element that contains the path to the temporary directory (as a URL) when found or an empty `c:result` if not.

```
<p:import href="http://xml.corbas.co.uk/xml/xproc-tools/temp-dir.xpl">
<ccproc:temp:dir name="get-temp-dir"/>
<p:identity/>
```

```xml
<c:result>file:///tmp/</c:result>
```

### ccproc:temp-file ###

This step creates a temporary file, following the same arguments as the EXProc `pdf:tempfile` step except that the system temporary directory generated by `ccproc:temp-dir` is used  as the temporary file location.

See [pxf:tempfile](http://exproc.org/proposed/steps/fileutils.html#tempfile) for additional documentation.

## directory-list.xpl ##

Import as  [http://xml.corbas.co.uk/xml/xproc-tools/directory-list.xpl](http://xml.corbas.co.uk/xml/xproc-tools/directory-list.xpl)

###  ccproc:directory-list ###

```xml
<p:declare-step type="ccproc:directory-list">
  <p:output port="result"/>
  <p:option name="path" required="true"/>
  <p:option name="resolve" select="'false'"/>
  <p:option name="match-path" select="'false'"/>
  <p:option name="include-filter"/>
  <p:option name="exclude-filter"/>
</p:declare-step>
```

This step slightly extends the standard `p:directory-list` step. 

Firstly, it allows the include and exclude patterns to operate on any part of the file or path name and not to match all of it. Secondly, it does not exclude directories under any circumstance. Directories always pass filtering.

####path
The path option should point to a directory on the current filesystem. It is down to the underlying implementation as to whether URL schemes bar _file:_ are supported.

```xml
<p:with-option name="path" 
  select="'file:///etc/'">
```

#### match-path ####

If set to _true_ then the `include-filter` and `exclude-filter` options will be applied to the entire path of a file. By default, these are only applied to the file name itself.

```xml
<ccproc:directory-listing path="file:///etc/" match-path="true"/>
```

#### include-filter ####

In most ways the `include-filter` option is identical to that specified for the built-in `p:directory-list` step. [Documentation](http://www.w3.org/TR/xproc/#c.directory-list) for that step applies. 

However, the regular expression is not required to match the whole file name or path.

```
<ccproc:directory-listing path="file:///etc/" 
  include-path="\.xml$"/>
```

#### exclude-filter ####

In most ways the `exclude-filter` option is identical to that specified for the built-in `p:directory-list` step. [Documentation](http://www.w3.org/TR/xproc/#c.directory-list) for that step applies. 

However, the regular expression is not required to match the whole file name or path.

```
<ccproc:directory-listing path="file:///etc/" 
  exclude-filter="\.tmp\.xml$"/>
```

**Note** that if both `include-filter` and `exclude-filter` options are provided, `include-filter` will be executed first.

#### resolve ####

If the `resolve` option is set to _true_ then all files and directories will be fully resolved. An additional attribute (`@uri`) will be created on each entry in the result set 

__Basic listing__
```xml
<p:import 
  href="http://xml.corbas.co.uk/xml/xproc-tools/directory-list.xpl">

<ccproc:directory-list name="dl" path="." include-filter="\.x[mp]l"/>

<p:identity>
  <p:input port="source">
    <p:pipe port="result" step="dl"/>
  </p:input>
</p:identity>
```


```xml
<c:directory name="src" 
  xml:base="file:/projects/xml/xproc-tools/src/">
  <c:file name="directory-list.xpl"/>
  <c:file name="load-sequence-from-file.xpl"/>
  <c:file name="recursive-directory-list.xpl"/>
  <c:file name="temp-dir.xpl"/>
  <c:file name="threaded-xslt.xpl"/>
</c:directory>
```

__With path resolution__

```xml
<ccproc:directory-list name="dl" path="." 
  resolve="true" include-filter="\.x[mp]l"/>

<p:identity>
  <p:input port="source">
    <p:pipe port="result" step="dl"/>
  </p:input>
</p:identity>
```

```xml
<c:directory name="src" 
  xml:base="file:/projects/xml/xproc-tools/src/">
  <c:file name="directory-list.xpl"
    uri="file:/projects/xml/xproc-tools/src/directory-list.xpl"/>
  <c:file name="load-sequence-from-file.xpl"
    uri="file:/projects/xml/xproc-tools/src/load-sequence-from-file.xpl"/>
  <c:file name="recursive-directory-list.xpl"
    uri="file:/projects/xml/xproc-tools/src/recursive-directory-list.xpl"/>
  <c:file name="temp-dir.xpl"
    uri="file:/projects/xml/xproc-tools/src/temp-dir.xpl"/>
  <c:file name="threaded-xslt.xpl"
    uri="file:/projects/xml/xproc-tools/src/threaded-xslt.xpl"/>
</c:directory>
```

## recursive-directory-list.xpl ##

Import as  [http://xml.corbas.co.uk/xml/xproc-tools/recursive-directory-list.xpl](http://xml.corbas.co.uk/xml/xproc-tools/recursive-directory-list.xpl)

## load-sequence-from-file.xpl ##

Many tasks require processing a sequence of documents in some way. We found ourselves writing processes where XML documents were fed through a sequence of stylesheets. After writing what was effectively the same script a few times, we got bored and wrote a script to load the stylesheets from a manifest file. A little while later, we realised that it was more general than that and stripped out the XSLT specific bits. 

As time and projects went by, it got a little more sophisticated.


### ccproc:load-sequence-from-file ###

Import as  [http://xml.corbas.co.uk/xml/xproc-tools/load-sequence-from-file.xpl](http://xml.corbas.co.uk/xml/xproc-tools/load-sequence-from-file.xpl)


```xml
<p:declare-step type="ccproc:load-sequence-from-file">
	<p:input port="source" primary="true"/>
	<p:output port="result" primary="true" result="true"/>
</p:declare-step>
```

This step takes a single input – the manifest file and returns a sequence of XML documents loaded from the definitions in that file. The manifest is a file that validates against [manifest.rng]((http://xml.corbas.co.uk/xml/schemas/manifest.rng). 

**The most recent version of the schema can always be accessed via [http://xml.corbas.co.uk/xml/schemas/manifest.rng](http://xml.corbas.co.uk/xml/schemas/manifest.rng)**

#### Using the manifest file ####

The manifest file allows the user to define a series of XML files to be loaded as a sequence. There are two ways to load files - directly or as the result of an XSLT stylesheet.  

The root of the manifest file is always a `manifest` element:

```xml
<manifest xmlns="http://www.corbas.co.uk/ns/transforms/data">
…
</manifest>
```

In its simplest form a manifest consists of sequence of `item` elements referencing XML files:

```xml
<manifest xmlns="http://www.corbas.co.uk/ns/transforms/data">
  <item href="doc1.xml"/>
  <item href="doc2.xml"/>
</manifest>
```

The result of processing this manifest would be a sequence of two XML documents containing the content of _doc1.xml_ followed by the content of  _doc2.xml_.

Components in the manifest may be grouped and may be given an `xml:id` attribute:

```xml
<manifest xmlns="http://www.corbas.co.uk/ns/transforms/data">
  <item href="doc1.xml"/>
  <group xml:id="group1">
    <item href="doc2.xml"/>
    <item href="doc3.xml"/>
  </group>
</manifest>
```

You can apply a description to any element:

```xml
<manifest xmlns="http://www.corbas.co.uk/ns/transforms/data">
  <item href="doc1.xml" description="Initial document"/>
  <item href="doc3.xml" description="Update document"/>
</manifest>
```

You can disable any element and it will be ignored (along with any descendants). Elements are considered to be enabled unless the `enabled` attribute is explicitly set to false:

```xml
<manifest xmlns="http://www.corbas.co.uk/ns/transforms/data">
  <item href="doc1.xml" enabled="false"/>
  <item href="doc3.xml" />
</manifest>
```

You an import a group (or a manifest):

```xml
<manifest xmlns="http://www.corbas.co.uk/ns/transforms/data">
  <item href="doc1.xml" enabled="false"/>
  <import href="default-manifest.xml" />
</manifest>
```

##### Processed items #####

One of the more sophisticated features of the loader script is that it can process and `item` using an XSLT stylesheet and output the result of that. We use this when generating XML documents on the fly as part of pipelines. It solves an issue where the inputs are predictable but multiple stages are needed to produce them.  In general, we have found that there is only one preprocessing step required. If more steps are needed, this may not be the right approach to solving your problem.

```xml
<manifest xmlns="http://www.corbas.co.uk/ns/transforms/data">
  <processed-item stylesheet="mapper.xsl">
    <item href="data01.xml"/>
  </processed-item>
  <item href="data-02.xml"/>
</manifest>
```

The result of loading this manifest would be a sequence of two documents,  the output of processing _data-01.xml_ with _mapper.xsl_ and _data-02.xml_.  Only the XSLT's primary output is used, any secondaries (via `xsl:result-document`) will be discarded.

##### Metadata #####

The final feature worth discussing is `metadata` elements.  These elements can be inserted at any point in the document:

```xml
<manifest xmlns="http://www.corbas.co.uk/ns/transforms/data">
  <item href="doc1.xml" enabled="false">
    <metadata name="param1" value="value1"/>
    <metadata name="param2" value="value2"/>
  </item>
  <metadata name="param2" value="value22"/> 
  <item href="doc2.xml">
    <metadata name="param1" value="value2"/>
  </item>
</manifest>
```

Metadata is assigned to items via the document hierarchy and not the document order. If two `metadata` elements in a hierarchy share the same `name` attribute then the lowest hierarchical value will be used.  This means that the effective metadata for the above would be:

```xml
<manifest xmlns="http://www.corbas.co.uk/ns/transforms/data">
  <item href="doc1.xml" enabled="false">
    <metadata name="param1" value="value1"/>
    <metadata name="param2" value="value2"/>
  </item>
  <item href="doc2.xml">
    <metadata name="param2" value="value22"/> 
    <metadata name="param1" value="value2"/>
  </item>
</manifest>
```

When the documents referenced by the `item` attributes are loaded, the  metadata is converted into namespaced attributes on the root element.  The attributes are in the namespace `http://www.corbas.co.uk/ns/transforms/data` with the prefix set to `data`. The attributes name is  constructed from the value of the `name` attribute  of the `metadata` element and the `data` prefix. 

If _doc1.xml_ above were to be as follows —

```xml
<document xmlns="http://example.com" xml:id="abc">
	<para>…</para>
</document>
```

then the result of loading it would be —

```xml
<document xmlns="http://example.com" xml:id="abc"
 xmlns:data="http://www.corbas.co.uk/ns/transforms/data"
 data:param1="value1" data:param2="value2">
	<para>…</para>
</document>
```

#### Other information ####

All elements may have the following attributes:

* `description`
* `xml:id`
* `enabled`

`group` elements may be nested and `import` elements may be included in groups.

Multiple `item` elements may be wrapped with a single `processed-item` element.

#### Integration with other modules ####

This module was specifically written with the _ccproc:threaded-xslt_ step in mind. When used with that module, the `item` elements will reference stylesheets. The _ccproc:threaded-xslt_ step  module is aware of the metadata attributes discussed above and they are converted to XSLT parameters and passed to the stylesheets when they evaluated.

## threaded-xslt.xpl ##

This module provides a solution to the problem of taking an input document and feeding it into a sequence of stylesheets where the output of a given stylesheet becomes the input to the next in the sequence.

### ccproc:threaded-xslt ###

Import as  [http://xml.corbas.co.uk/xml/xproc-tools/threaded-xslt.xpl](http://xml.corbas.co.uk/xml/xproc-tools/threaded-xslt.xpl)


```xml
<p:declare-step type="ccproc:threaded-xslt">
	<p:input port="source" primary="true"/>
	<p:input port="stylesheets" sequence="true"/>
	<p:input port="parameters" kind="parameter" 
	  primary="true"/>
	<p:output port="result" primary="true"/>
	<p:output port="intermediates" sequence="truee"/>
</p:declare-step>
```

The step takes two input ports. The primary input (`source`) holds the document to be transformed. The other input port (`stylesheets`) holds the sequence of stylesheets to be applied to the source document. 

The step applies the first stylesheet to the input document, the second stylesheet to the output of the first and so on.

The final output is presented on the `result` port. However, all intermediate output is available on the `imtermediates` port.

```xml
<p:import href="http://xml.corbas.co.uk/xml/xproc-tools/threaded-xslt.xpl"/>
<ccproc:threaded-xslt>
  <p:input port="source">
    <p:inline><test-doc>test content</test-doc></p:inline>
  </p:input>
  <p:input port="stylesheets">
    <p:document href="transform-01.xsl"/>
    <p:document href="transform-02.xsl"/>
  </p:input>
</ccproc:threaded-xslt>
```

The output on the `result` port would be the result of transforming the document on the input port with _transform-01.xsl_ and then transforming the output of that transformation with _transform-01.xsl_. 

The output on the `intermediates` port would be a sequence of two documents. The first would be the result of transforming the input document with _transform-01.xsl_ and then the result of transforming that document with _transform-02.xsl_. Obviously, the intermediates port has  more value if more documents are transformed. The intent of the intermediates port is to allow debug output to be created.

#### Metadata and parameters ####

This step can operate in conjunction with _ccproc:load-sequence-from-file_ to convert metadata stored in the manifest into XSLT parameter values. 

_ccproc:load-sequence-from-file_ examines the XSLT documents looking for attributes on the root element in the `http://www.corbas.co.uk/ns/transforms/data` namespace and creates parameters by stripping the namespace from the attribute to get a name and using the value as the parameter value.

Given a manifest —

```xml
<manifest xmlns="http://www.corbas.co.uk/ns/transforms/data">
  <metadata name="input-root" value="/usr/local/share/xml/"/>
  <item href="transform-01.xsl" enabled="false"/>  
  <item href="transfor-02.xsl">
    <metadata name="output-root" value="/var/www/docs/"/>
  </item>
</manifest>
```

_ccproc:threaded-xslt_ will create XSLT parameters and pass them to the stylesheet engine. When _transform-01.xsl_ is applied to a document, the parameter `input-root` will be set to the value "/usr/local/share/xml/" . When _transform-02.xsl_ is applied, `input-root` will also be set (to "/usr/local/share/xml/") and `output-root` will be set to "/var/www/docs/".
