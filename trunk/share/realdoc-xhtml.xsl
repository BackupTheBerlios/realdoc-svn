<?xml version="1.0" encoding="ISO-8859-1"?>
<!--
Copyright 2006  Peter Gebauer
(see LICENSE.txt for licensing information)

XSLT Stylesheet for transforming realdoc XML to XHTML.
-->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="http://www.w3.org/1999/xhtml">
  <xsl:output
      method="xml"
      indent="yes"
      encoding="ISO-8859-1"
      doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" 
      doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
      />

  <xsl:param name='index'>.</xsl:param>
  <xsl:variable name="topAName">d8e8fca2dc0f896fd7cb4cb0031ba249</xsl:variable>

  <xsl:template match="realdoc">
    <html>
      <head>
        <title>
          <xsl:value-of select="meta[@name='title']"/>
          <xsl:if test="package">
            - <xsl:value-of select="package/@name"/>
          </xsl:if>
          <xsl:if test="module">
            - <xsl:value-of select="module/@name"/>
          </xsl:if>
        </title>
        <style type="text/css">
          p { margin-top: 0px }
          div.indent { margin-left: 4em }
          h4 { color: #4080D0; margin-bottom: 0px }
          span.path { font-size: small; font-style: italic }
        </style>
      </head>
      <body>
        <a name="{$topAName}"/>
        <h1>
          <xsl:value-of select="meta[@name='title']"/>
        </h1>
        <xsl:choose>
          <xsl:when test="index">
            <div class="index">
              <h2>Index</h2>
              <dl>
                <xsl:apply-templates select="index"/>
              </dl>
            </div>
          </xsl:when>
          <xsl:otherwise>
            <a href="{$index}/index.html">
              Back to Index
            </a>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select="package"/>
        <xsl:apply-templates select="module"/>
        <hr/>
        <p>
          <span class="copyright">
            <xsl:value-of select="meta[@name='copyright']"/>
          </span>
        </p>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="package">
    <div class="package">
      <a name="{@path}"/>
      <h2 class="package">Package <xsl:value-of select="@name"/></h2>
      <p>
        Path:
        <span class="path"><xsl:value-of select="@path"/></span>
      </p>
      <xsl:if test="substring(@path, 0, string-length(@path) - string-length(@name))">
        <p>
          Parent:
          <a href="../__init__.html">
            <span class="path">
              <xsl:value-of 
                  select="substring(@path, 0, string-length(@path) - string-length(@name))"/>
            </span>
          </a>
        </p>
      </xsl:if>
      <p class="doc">
        <xsl:value-of disable-output-escaping="yes" select="doc"/>
      </p>
      <h3>Contents:</h3>
      <dl>
        <xsl:for-each select="subpackage">
          <dd>
            Package
            <xsl:variable name="link">
              <xsl:value-of 
                  select="translate(substring-after(@path,  concat(../@path, '.')), '.', '/')"/>
            </xsl:variable>
            <a href="{$link}/__init__.html">
              <xsl:value-of select="$link"/>
            </a>:
            <xsl:value-of disable-output-escaping="yes" 
                          select="substring-before(doc, '&lt;br/&gt;')"/>
          </dd>
        </xsl:for-each>
        <xsl:for-each select="submodule">
          <dd>
            Module
            <xsl:variable name="link">
              <xsl:value-of 
                  select="translate(substring-after(@path,  concat(../@path, '.')), '.', '/')"/>
            </xsl:variable>
            <a href="{$link}.html">
              <xsl:value-of select="$link"/>
            </a>:
            <xsl:value-of disable-output-escaping="yes" 
                          select="substring-before(doc, '&lt;br/&gt;')"/>
          </dd>
        </xsl:for-each>
        <xsl:for-each select="class">
          <dd>
            Class <a href="#{@path}"><xsl:value-of select="@name"/></a>:
            <xsl:value-of disable-output-escaping="yes" 
                          select="substring-before(doc, '&lt;br/&gt;')"/>
          </dd>
        </xsl:for-each>
        <xsl:for-each select="def">
          <dd>
            Function <a href="#{@path}"><xsl:value-of select="@name"/></a>:
            <xsl:value-of disable-output-escaping="yes" 
                          select="substring-before(doc, '&lt;br/&gt;')"/>
          </dd>
        </xsl:for-each>
      </dl>
      <xsl:if test="class">
        <h3>Classes:</h3>
        <xsl:apply-templates select="class"/>
      </xsl:if>
      <xsl:if test="def">
        <h3>Functions:</h3>
        <xsl:apply-templates select="def"/>
      </xsl:if>
    </div>
  </xsl:template>

  <xsl:template match="module">
    <div class="module">
      <a name="{@path}"/>
      <h2 class="module">Module <xsl:value-of select="@name"/></h2>
      <p>
        Path:
        <span class="path"><xsl:value-of select="@path"/></span>
      </p>
      <xsl:if test="substring(@path, 0, string-length(@path) - string-length(@name))">
        <p>
          Parent:
          <a href="./__init__.html">
            <span class="path">
              <xsl:value-of 
                  select="substring(@path, 0, string-length(@path) - string-length(@name))"/>
            </span>
          </a>
        </p>
      </xsl:if>
      <p class="doc">
        <xsl:value-of disable-output-escaping="yes" select="doc"/>
      </p>
      <h3>Contents:</h3>
      <dl>
        <xsl:for-each select="class">
          <dd>
            Class <a href="#{@path}"><xsl:value-of select="@name"/></a>:
            <xsl:value-of disable-output-escaping="yes" 
                          select="substring-before(doc, '&lt;br/&gt;')"/>
          </dd>
        </xsl:for-each>
        <xsl:for-each select="def">
          <dd>
            Function <a href="#{@path}"><xsl:value-of select="@name"/></a>:
            <xsl:value-of disable-output-escaping="yes" 
                          select="substring-before(doc, '&lt;br/&gt;')"/>
          </dd>
        </xsl:for-each>
      </dl>
      <xsl:if test="./class">
        <h3>Classes:</h3>
        <div class="indent">
          <xsl:apply-templates select="class"/>
        </div>
      </xsl:if>
      <xsl:if test="./def">
        <h3>Functions:</h3>
        <div class="indent">
          <xsl:apply-templates select="def"/>
        </div>
      </xsl:if>
    </div>
  </xsl:template>

  <xsl:template match="class">
    <div class="class">
      <a name="{@path}"/><h4 class="class">
        class <xsl:value-of select="@name"/><xsl:if test="ancestor">(<xsl:for-each select="ancestor"><xsl:if test="position() > 1">, </xsl:if><xsl:value-of select="."/></xsl:for-each>)</xsl:if>
      </h4>
      <div class="indent">
        <p class="doc">
          <xsl:value-of disable-output-escaping="yes" select="doc"/>
        </p>
        <xsl:if test="class">
          <xsl:apply-templates select="class"/>
        </xsl:if>
        <xsl:if test="def">
          <xsl:apply-templates select="def"/>
        </xsl:if>
      </div>
      <p>
        [<a href="#{$topAName}">Top of page</a>] [parent
        <a href="#{substring-before(@path, concat('.', @name))}">
          <xsl:value-of select="substring-before(@path, concat('.', @name))"/>
        </a>]
      </p>
    </div>
  </xsl:template>

  <xsl:template match="def">
    <div class="def">
      <a name="{@path}"/><h4 class="def">
        def <xsl:value-of select="@name"/><xsl:if test="arg">(<xsl:for-each select="arg"><xsl:if test="position() > 1">, </xsl:if><xsl:choose><xsl:when test="@type='dict'">**</xsl:when><xsl:when test="@type='list'">*</xsl:when></xsl:choose><xsl:value-of select="."/><xsl:if test="@default"> = <xsl:value-of select="@default"/></xsl:if></xsl:for-each>)</xsl:if>
      </h4>
      <div class="indent">
        <p class="doc">
          <xsl:value-of disable-output-escaping="yes" select="doc"/>
        </p>
      </div>
      <p>
        [<a href="#{$topAName}">Top of page</a>] [parent
        <a href="#{substring-before(@path, concat('.', @name))}">
          <xsl:value-of select="substring-before(@path, concat('.', @name))"/>
        </a>]
      </p>
    </div>
  </xsl:template>

  <xsl:template match="index">
    <dd>
      <p>
      <xsl:choose>
        <xsl:when test="@type='package'">
          Package
          <a href="{translate(@path, '.', '/')}/__init__.html">
            <xsl:value-of select="@path"/>
          </a>
          <xsl:if test="normalize-space(doc)">
            : <xsl:value-of disable-output-escaping="yes" select="doc"/>
          </xsl:if>
        </xsl:when>
        <xsl:when test="@type='module'">
          Module
          <a href="{translate(@path, '.', '/')}.html">
            <xsl:value-of select="@path"/>
          </a>
          <xsl:if test="normalize-space(doc)">
            : <xsl:value-of disable-output-escaping="yes" select="doc"/>
          </xsl:if>
        </xsl:when>
        <xsl:otherwise>UNSUPPORTED?!</xsl:otherwise>
      </xsl:choose>
      </p>
    </dd>
  </xsl:template>

</xsl:stylesheet>

