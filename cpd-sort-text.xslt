<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:cpd="https://pmd-code.org/schema/cpd-report"
  exclude-result-prefixes="cpd">

  <xsl:output method="text" encoding="UTF-8"/>

  <xsl:template match="/cpd:pmd-cpd">
    <xsl:text>CPD duplicates (sorted by tokens, lines)</xsl:text>
    <xsl:text>&#10;&#10;</xsl:text>

    <xsl:for-each select="cpd:duplication">
      <xsl:sort select="@tokens" data-type="number" order="ascending"/>
      <xsl:sort select="@lines"  data-type="number" order="ascending"/>

      <xsl:text>==================================================&#10;</xsl:text>
      <xsl:text>Tokens: </xsl:text><xsl:value-of select="@tokens"/>
      <xsl:text>   Lines: </xsl:text><xsl:value-of select="@lines"/>
      <xsl:text>   Occurrences: </xsl:text><xsl:value-of select="count(cpd:file)"/>
      <xsl:text>&#10;</xsl:text>

      <xsl:text>Files:&#10;</xsl:text>
      <xsl:for-each select="cpd:file">
        <xsl:text>  - </xsl:text>
        <xsl:value-of select="@path"/>
        <xsl:text> : </xsl:text>
        <xsl:value-of select="@line"/>
        <xsl:text>–</xsl:text>
        <xsl:value-of select="@endline"/>
        <xsl:text>&#10;</xsl:text>
      </xsl:for-each>

      <xsl:text>&#10;</xsl:text>
      <xsl:text>Snippet:&#10;</xsl:text>
      <xsl:value-of select="cpd:codefragment"/>
      <xsl:text>&#10;&#10;</xsl:text>
    </xsl:for-each>
    <xsl:text>==================================================&#10;</xsl:text>
    <xsl:text>Total duplicate groups: </xsl:text>
    <xsl:value-of select="count(cpd:duplication)"/>
    <xsl:text>&#10;</xsl:text>
  </xsl:template>

</xsl:stylesheet>

