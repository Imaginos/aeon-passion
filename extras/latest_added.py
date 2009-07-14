import xbmc
from xbmcgui import Window
from urllib import quote_plus
import re
# limit number to
RECENT_NUMBER = 4
# grab the home window
WINDOW = Window( 10000 )
# sql statements
sql_movies = "select * from movieview order by idMovie desc limit %d" % ( RECENT_NUMBER, )
sql_episodes = "select * from episodeview order by idepisode desc limit %d" % ( RECENT_NUMBER, )
#sql_tvshowlinkepisode = "select idshow from tvshowlinkepisode where idEpisode=%u" % ( fields[ 13 ], )
# format our records start and end
xbmc.executehttpapi( "SetResponseFormat(OpenRecord,%s)" % ( "<record>", ) )
xbmc.executehttpapi( "SetResponseFormat(CloseRecord,%s)" % ( "</record>", ) )
# query the database
movies_xml = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql_movies ), )
episodes_xml = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql_episodes ), )
# separate the records
movies = re.findall( "<record>(.+?)</record>", movies_xml, re.DOTALL )
episodes = re.findall( "<record>(.+?)</record>", episodes_xml, re.DOTALL )
# enumerate thru our records and set our properties
for count, movie in enumerate( movies ):
    # separate individual fields
    fields = re.findall( "<field>(.*?)</field>", movie, re.DOTALL )
    # set title
    WINDOW.setProperty( "LatestMovie.%d.Label" % ( count + 1, ), fields[ 1 ] )
    # set year
    WINDOW.setProperty( "LatestMovie.%d.Label2" % ( count + 1, ), fields[ 8 ] )
    # set running time (uncomment below if you want running time for label2)
    #WINDOW.setProperty( "LatestMovie.%d.Label2" % ( count + 1, ), fields[ 12 ] )
    # set path
    WINDOW.setProperty( "LatestMovie.%d.OnClick" % ( count + 1, ), fields[ 24 ] + fields[ 23 ] )
    # set thumbnail
    thumbnail = xbmc.getCacheThumbName( fields[ 24 ] + fields[ 23 ] )
    WINDOW.setProperty( "LatestMovie.%d.Thumb" % ( count + 1, ), "special://profile/Thumbnails/Video/%s/%s" % ( thumbnail[ 0 ], thumbnail, ) )
# enumerate thru our records and set our properties
for count, episode in enumerate( episodes ):
    # separate individual fields
    fields = re.findall( "<field>(.*?)</field>", episode, re.DOTALL )
    # set title
    WINDOW.setProperty( "LatestEpisode.%d.Label" % ( count + 1, ), fields[ 1 ] )
    # get tvshow name
    tvshowlinkepisode_xml = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( "select tvshow.c%02d from tvshow,tvshowlinkepisode where tvshowlinkepisode.idepisode=%d and tvshowlinkepisode.idshow=tvshow.idshow" % ( 0, int( fields[ 0 ] ), ) ), )
    tvname = tvshowlinkepisode_xml.replace('<record><field>','')
    tvname = tvname.replace('</field></record>','')
    # set season/episode
    WINDOW.setProperty( "LatestEpisode.%d.Label2" % ( count + 1, ), tvname + " - s%02de%02d" % ( int( fields[ 13 ] ), int( fields[ 14 ] ), ) )
    # set path
    WINDOW.setProperty( "LatestEpisode.%d.OnClick" % ( count + 1, ), fields[ 24 ] + fields[ 23 ] )
    # set thumbnail
    thumbnail = xbmc.getCacheThumbName( fields[ 24 ] + fields[ 23 ] )
    WINDOW.setProperty( "LatestEpisode.%d.Thumb" % ( count + 1, ), "special://profile/Thumbnails/Video/%s/%s" % ( thumbnail[ 0 ], thumbnail, ) )  