from __future__ import print_function
from Adafruit_Thermal import *
from xml.dom.minidom import parseString
import itertools
import json
import re
import urllib2
import time

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
today = time.strftime("%Y-%m-%d")

text = urllib2.urlopen('http://dcsd.nutrislice.com/menu/eldorado/lunch/').read()
menus = json.loads(re.search(r"bootstrapData\['menuMonthWeeks'\]\s*=\s*(.*);", text).group(1))
days = itertools.chain.from_iterable(menu['days'] for menu in menus)
day = next(itertools.dropwhile(lambda day: day['date'] != today, days), None)

if day:

    printer.inverseOn()
    printer.print('{:^32}'.format("Lunch menu for " + today))
    printer.inverseOff()

    menu_items = '\n'.join(item['food']['name'] for item in day['menu_items'])
    printer.print(menu_items)

    printer.feed(3)
    print(menu_items)

else:
    print('Day not found.')