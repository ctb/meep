#!/usr/bin/env python
"""
"""

import os
import quixote
from quixote.publish import Publisher
from quixote.directory import Directory
from quixote.util import StaticDirectory
import urllib
import pprint
import json

from bs4 import BeautifulSoup           # the BeautifulSoup package
                                        # for Web scraping

def get_closest_stop(lat, lon):
    url = 'http://tp.cata.org/hiwire?.a=iStopLookupClosest'

    lat = int(float(lat) * 1e6)
    lon = int(float(lon) * 1e6)

    d = {}
    #d['StartGeo'] = 'YOUR LOCATION;-84427589;42744482' # okemos & raby, 2931
    d['StartGeo'] = 'YOUR LOCATION;%s;%s' % (lon, lat)

    qs = urllib.urlencode(d)
    the_html = urllib.urlopen(url + '&' + qs).read()

    soup = BeautifulSoup(the_html)
    table = soup.find('table', { 'class' : 'location-table'})
    stop_info = table.find('td').find('b').get_text()
    stop_info = stop_info.strip()

    stop_number = None
    if stop_info.startswith('Stop #'):
        stop_number = int(stop_info[6:])
        print 'XXX', stop_number

    #stop_number = 2931                    # okemos & raby
    return stop_number

def get_next_bus_time(stop_number):
    url = 'http://tp.cata.org/hiwire?.a=iNextBusMatch&ShowTimes=1&NumStopTimes=5&GetSchedules=1&NextBusText=%(stop_number)s&Date=%(datestr)s&HourDropDown=%(hour)s&MinuteDropDown=%(min)s&MeridiemDropDown=p&SB=Get+Stop+Details'

    datestr = '04-19-2012'
    hour = 13
    min = 50
    stop_number = 2931                    # okemos & raby

    url = url % dict(stop_number=stop_number, datestr=datestr, hour=hour,
                     min=min)

    the_html = urllib.urlopen(url).read()

    soup = BeautifulSoup(the_html)
    table = soup.find('table', { 'class' : 'options-table'})
    tr = table('tr')[1]
    time, route_num, route_name = [ x.get_text().strip() \
                                    for x in tr('td') ][:3]

    return dict(time=time, route_num=route_num, route_name=route_name)

class RootDirectory(Directory):

    _q_exports = ['', 'get_next_bus', 'html']

    html = StaticDirectory(os.path.abspath('./html'))

    def _q_index(self):
        request = quixote.get_request()
        return quixote.redirect('./html/index.html')

    def get_next_bus(self):
        request = quixote.get_request()
        response = quixote.get_response()
        response.set_content_type('application/json')
        form = request.form

        #return """{"route_num": "22", "stop_number": 2586, "route_name": "HASLETT-MERIDIAN MALL-MSU", "time": "6:17a"}"""

        lat = form['lat']
        lon = form['lon']
        stop_number = get_closest_stop(lat, lon)
        data = get_next_bus_time(stop_number)
        data['stop_number'] = stop_number
        
        x = json.dumps(data)
        return x

def create_publisher():
    return Publisher(RootDirectory(),
                     display_exceptions='plain')


if __name__ == '__main__':
    from quixote.server.simple_server import run
    print 'creating demo listening on http://localhost:8000/'
    run(create_publisher, host='localhost', port=8000)
