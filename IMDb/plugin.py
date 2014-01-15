###
# Copyright (c) 2012, Dan
# All rights reserved.
#
#
###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

import json
import socket
import urllib2
import unicodedata
from lxml import html
from urllib import urlencode

def unid(s):
    if isinstance(s, unicode):
        return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
    else:
        return s

class IMDb(callbacks.Plugin):
    """Add the help for "@plugin help IMDb" here
    This should describe *how* to use this plugin."""
    threaded = True

    def __init__(self, irc):
        self.__parent = super(IMDb, self)
        self.__parent.__init__(irc)

    def randomimdb(self, irc, msg, args):
        """output info from IMDb about a random popular title """
		
        req = urllib2.Request('http://www.imdb.com/random/title')
		
        try:
            page = urllib2.urlopen(req)
        except socket.timeout, e:
            irc.error('\x0304Connection timed out.\x03', prefixNick=False)
            return
        except urllib2.HTTPError, e:
            irc.error('\x0304HTTP Error\x03', prefixNick=False)
            return
        except urllib2.URLError, e:
            irc.error('\x0304URL Error\x03', prefixNick=False)
            return
			
        finalurl = page.geturl()
        self._imdbinfo(irc, finalurl)

    randomimdb = wrap(randomimdb)
    whatshouldiwatch = randomimdb
		
		
    def imdb(self, irc, msg, args, opts, text):
        """<movie>
        output info from IMDb about a movie"""

        textencoded = urlencode({'q': 'site:http://www.imdb.com/title/ %s' % text})
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (textencoded)
        request = urllib2.Request(url)
        try:
            page = urllib2.urlopen(request)
        except socket.timeout, e:
            irc.error('\x0304Connection timed out.\x03', prefixNick=False)
            return
        except urllib2.HTTPError, e:
            irc.error('\x0304HTTP Error\x03', prefixNick=False)
            return
        except urllib2.URLError, e:
            irc.error('\x0304URL Error\x03', prefixNick=False)
            return

        result = json.load(page)

        if result['responseStatus'] != 200:
            irc.error('\x0304Google search didnt work, returned status %s' % result['responseStatus'])
            return

        imdb_url = None

        for r in result['responseData']['results']:
            if r['url'][-1] == '/':
                imdb_url = r['url']
                break

        if imdb_url is None:
            irc.error('\x0304Couldnt find a title')
            return 
		
	self._imdbinfo(irc, imdb_url)
			
    imdb = wrap(imdb, [getopts({'s': '', 'short': ''}), 'text'])

    def _imdbinfo(self, irc, imdb_url):
        request = urllib2.Request(imdb_url, 
                headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:5.0) Gecko/20100101 Firefox/5.0',
                        'Accept-Language': 'en-us,en;q=0.5'})
        try:
            page = urllib2.urlopen(request)
        except socket.timeout, e:
            irc.error('\x0304Connection timed out.\x03', prefixNick=False)
            return
        except urllib2.HTTPError, e:
            irc.error('\x0304HTTP Error\x03', prefixNick=False)
            return
        except urllib2.URLError, e:
            irc.error('\x0304URL Error\x03', prefixNick=False)
            return

        root = html.parse(page)

        elems = root.xpath('//h1/span[@itemprop="name"]|//div[h4="Genres:"]')

        title = unid(elems[0].text.strip())
        genres = unid( ' '.join(elems[1].text_content().split()).strip().replace('Genres: ', ''))

        elem = root.xpath('//div[h4="Stars:"]')
        if elem:
            stars = unid(' '.join(elem[0].text_content().split()).replace('Stars: ', '').replace(' | See full cast and crew', ''))
        else:
            stars = 'N/A'

        elem = root.xpath('//div[h4="Plot Keywords:"]')
        if elem:
            plot_keywords = unid(' '.join(elem[0].text_content().replace(u'\xbb', '').split()).strip().replace(' | See more', '').replace('Plot Keywords: ', ''))
        else:
            plot_keywords = 'N/A'

        elem = root.xpath('//h1[span/@itemprop="name"]/span[last()]/a')
        if elem:
            year = elem[0].text
        else:
            year = unid(root.xpath('//h1[span/@itemprop="name"]/span[last()]')[0].text.strip().strip(')(').replace(u'\u2013', '-'))

        elem = root.xpath('//div[@class="star-box-details"]/strong/span|//div[@class="star-box-details"]/span[@class="mellow"]/span')
        if elem:
            rating = ircutils.bold(elem[0].text) + '/' + elem[1].text
        else:
            rating = '-/10'

        elem = root.xpath('//p[@itemprop="description"]')
        if elem:
            description = elem[0].text_content()
            description = unid(description.replace(u'\xbb', '').strip().replace('See full summary', '').strip())
        else:
            description = 'N/A'

        elem = root.xpath('//div[@itemprop="director"]/a/span')
        if elem:
            director = unid(elem[0].text)
        else:
            director = 'N/A'

        elem = root.xpath('//div[h4="\n  Creator:\n  "]/a')
        if elem:
            creator = unid(elem[0].text)
        else:
            creator = 'N/A'

        elem = root.xpath('//div[h4="Runtime:"]/time')
        if elem:
            runtime = elem[0].text
        else:
            runtime = 'N/A'

        irc.reply('%s' % imdb_url, prefixNick=False)
        title = ircutils.bold(title)
        genreheader = ircutils.bold("Genre: ")
        plotheader = ircutils.bold("Plot: ")
        directorheader = ircutils.bold("Director: ")
        starsheader = ircutils.bold("Stars: ")
        irc.reply('%s (%s) %s || %s%s || %s%s || %s%s || %s%s' % (title, year, rating, genreheader, genres, plotheader, description, directorheader, director, starsheader, stars), prefixNick=False)
#        irc.reply(ircutils.bold(title) + " || " + ircutils.bold("Genre: ") + genres + " || " + rating + " ||  " + ircutils.bold("Plot: ") + summary)
#        if description:
#            irc.reply('\x0305Description\03 /\x0311 %s' % description, prefixNick=False)
#        if creator:
#            irc.reply('\x0305Creator\03 /\x0311 %s' % creator, prefixNick=False)
#
#        out = []
#        if director:
#            out.append('\x0305Director\03 /\x0311 %s' % director)
#        if stars:
#            out.append('\x0305Stars\x03 /\x0311 %s' % stars)
#        if out:
#            irc.reply(' '.join(out), prefixNick=False)
#
#        out = []
#        if genres:
#            out.append('\x0305Genres\03 /\x0311 %s' % genres)
#        if plot_keywords:
#            out.append('\x0305Plot Keywords\03 /\x0311 %s' % plot_keywords)
#        if out:
#            irc.reply('\x0305Genres\03 /\x0311 %s \x0305Plot Keywords\03 /\x0311 %s' % (genres, plot_keywords), prefixNick=False)
#
#        if runtime:
#            irc.reply('\x0305Runtime:\x03 %s' % runtime, prefixNick=False)


Class = IMDb


# vim:set shiftwidth=4 softtabstop=4 expandtab:
