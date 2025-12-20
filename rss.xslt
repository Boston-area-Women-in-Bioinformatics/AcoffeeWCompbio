<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
                xmlns:content="http://purl.org/rss/1.0/modules/content/"
                version="1.0">
    <xsl:output method="html" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN" />

    <xsl:variable name="title" select="/rss/channel/title" />
    <xsl:variable name="feedDesc" select="/rss/channel/description" />
    <xsl:variable name="copyright" select="/rss/channel/copyright" />

    <xsl:template match="/">
        <xsl:element name="html">
            <head>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <link href="rss-styles.css" rel="stylesheet" type="text/css" media="all" />
                <title>
                    <xsl:value-of select="$title" /> - RSS Feed
                </title>
            </head>
            <xsl:apply-templates select="rss/channel" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="channel">
        <body>
            <div class="container">
                <div class="top-block">
                    <div class="podcast-header">
                        <xsl:apply-templates select="image" />
                        <div class="top-description">
                            <h1>
                                <xsl:element name="a">
                                    <xsl:attribute name="href">
                                        <xsl:value-of select="/rss/channel/link[1]" xmlns:atom="http://www.w3.org/2005/Atom" />
                                    </xsl:attribute>
                                    <xsl:value-of select="$title" />
                                </xsl:element>
                            </h1>
                            <div class="rss-badge">
                                <span class="rss-icon">📻</span> RSS Feed Preview
                            </div>
                            <div class="description-block">
                                <div class="description">
                                    <p>
                                        <xsl:value-of select="$feedDesc" />
                                    </p>
                                    <p class="copyright">Copyright: <xsl:value-of select="$copyright" /></p>
                                    <div class="subscribe-info">
                                        <p><strong>Copy this feed URL to subscribe in your podcast player:</strong></p>
                                        <input type="text" readonly="readonly" class="feed-url-input" id="feedUrl" onclick="this.select()">
                                            <xsl:attribute name="value">
                                                <xsl:value-of select="/rss/channel/atom:link[@rel='self']/@href" xmlns:atom="http://www.w3.org/2005/Atom"/>
                                            </xsl:attribute>
                                        </input>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="episodes-section">
                    <h2>Episodes</h2>
                    <ul class="episode-list" xmlns="http://www.w3.org/1999/xhtml">
                        <xsl:apply-templates select="item" />
                    </ul>
                </div>
            </div>
        </body>
    </xsl:template>

    <xsl:template match="image">
        <div class="podcast-artwork">
            <a href="{link}" title="Visit podcast website">
                <xsl:element name="img" namespace="http://www.w3.org/1999/xhtml">
                    <xsl:attribute name="src">
                        <xsl:value-of select="url" />
                    </xsl:attribute>
                    <xsl:attribute name="alt">Podcast artwork</xsl:attribute>
                </xsl:element>
            </a>
        </div>
    </xsl:template>

    <!-- Episode item template -->
    <xsl:template match="item" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:atom="http://www.w3.org/2005/Atom">
        <li class="episode">
            <div class="episode-image">
                <xsl:element name="img" namespace="http://www.w3.org/1999/xhtml">
                    <xsl:attribute name="src">
                        <xsl:value-of select="itunes:image/@href" />
                    </xsl:attribute>
                    <xsl:attribute name="alt">Episode artwork</xsl:attribute>
                </xsl:element>
            </div>
            <article class="episode-content">
                <div class="episode-header">
                    <h3 class="episode-title">
                        <xsl:value-of select="title" />
                    </h3>
                    <p class="episode-meta">
                        <span class="episode-number">Episode <xsl:value-of select="itunes:episode" /></span>
                        <span class="separator">•</span>
                        <span class="episode-date">
                            <xsl:value-of select="substring(pubDate, 1, 16)" />
                        </span>
                        <span class="separator">•</span>
                        <span class="episode-duration">
                            <xsl:value-of select="itunes:duration" />
                        </span>
                    </p>
                </div>

                <xsl:element name="p" namespace="http://www.w3.org/1999/xhtml">
                    <xsl:attribute name="class">episode-description</xsl:attribute>
                    <xsl:value-of select="itunes:subtitle" />
                </xsl:element>

                <xsl:if test="count(child::enclosure)&gt;0">
                    <xsl:if test="contains(enclosure/@type, 'audio')">
                        <div class="audio-player">
                            <xsl:element name="audio" namespace="http://www.w3.org/1999/xhtml">
                                <xsl:attribute name="controls" />
                                <xsl:attribute name="preload">none</xsl:attribute>
                                <xsl:element name="source" namespace="http://www.w3.org/1999/xhtml">
                                    <xsl:attribute name="src">
                                        <xsl:value-of select="enclosure/@url" />
                                    </xsl:attribute>
                                    <xsl:attribute name="type">
                                        <xsl:value-of select="enclosure/@type" />
                                    </xsl:attribute>
                                </xsl:element>
                                Your browser does not support the audio element.
                            </xsl:element>
                            <xsl:element name="a" namespace="http://www.w3.org/1999/xhtml">
                                <xsl:attribute name="class">download-btn</xsl:attribute>
                                <xsl:attribute name="href">
                                    <xsl:value-of select="enclosure/@url" />
                                </xsl:attribute>
                                <xsl:attribute name="download" />
                                ⬇ Download
                            </xsl:element>
                        </div>
                    </xsl:if>
                </xsl:if>
            </article>
        </li>
    </xsl:template>

</xsl:stylesheet>
