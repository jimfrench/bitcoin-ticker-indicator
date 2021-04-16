#!/usr/bin/env python2

#Markus Lemm - 260444 - August 18, 2014
#Jim French - November 28, 2015
#Bitcoin indicator

import sys
import gtk
import appindicator
import urllib2
import os

REFRESH_PRICE = 60000

class checkBitCoinPrice:
    def __init__(self):
        self.ind = appindicator.Indicator("bitcoin-ticker-indicator", os.path.dirname(os.path.realpath(__file__)), appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_property('label-guide', "000.00")
        self.ind.set_label("000.00", "000.00")
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.menu_setup()
        self.ind.set_menu(self.menu)


    def menu_setup(self):
        self.menu = gtk.Menu()

        self.refresh = gtk.MenuItem("Refresh")
        self.refresh.connect("activate",self.manual_labelx)
        self.refresh.show()
        self.menu.append(self.refresh)

        self.exit = gtk.MenuItem("Exit")
        self.exit.connect("activate",self.exit_menu)
        self.exit.show()
        self.menu.append(self.exit)


    def exit_menu(self, widget):
        sys.exit(0) 


    def manual_labelx(self, widget):
        req = urllib2.Request('https://api.coindesk.com/v1/bpi/currentprice/GBP.json')

        try: #if not able to connect then just output 0.00
            response = urllib2.urlopen(req)
        except Exception:
            last_price = "0.00"
        else:
            the_page = response.read().split(",")
            last_price = the_page[13]

        last_price = last_price.replace("\"rate_float\":", "")
        last_price = last_price.replace("}}}", "")
        #rate_int = int(round(float(last_price.strip())))
        self.ind.set_label("= "u"\xA3" + str(last_price))
    
    def change_labelx(self):
        self.manual_labelx(self)
        return True #if set to False will only return once


    def main(self):
        self.change_labelx()
        gtk.timeout_add(REFRESH_PRICE, self.change_labelx)
        gtk.main()


if __name__ == "__main__":
    indicator = checkBitCoinPrice()
    indicator.main()
