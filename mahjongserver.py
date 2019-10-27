import urllib
import mahtml
import re
from HTMLTags import *

import time

   
def get_hand_form(sit=''):
    return FORM(INPUT(type="text", name="sit", value=sit, size=40) + 
                INPUT(type="submit", value="Calculate"), 
                method='get', action='')  + A("Main page", href='/')

def help_fragment():
    fragment = P(TEXT('Enter a situation and press "Calculate" (see ') + A('format', href='#format') + TEXT(' below)'))
    fragment += get_hand_form()
    fragment += P('Look at some of the sample hands to get started:')
    fragment += P(A("Try this for 45 points", href='/?sit=h 1234564567899b w 9b'))
    fragment += P(A("Crazy hand", href='/?sit=c Weeee Wssss Wwwww Wnnnn h Dr w Dr'))
    baseline_hands = [
        ('Hand 1', 47, 'm 333d h 1116667772d w 2d'),
        ('Hand 2', 12, 'm 657b h 345678d4456c w 4c self_draw'),
        ('Hand 3', 6, 'm 234b 234d h 567b567dDg w gD self_draw'),
        ('Hand 4', 64, 'h 11d99brrDssWggD11c1d w 1d'),
        ('Hand 5', 24, 'h 1c258d369bwsenWgrD w Dw'),
        ('Hand 6', 23, 'm 123b 456b 789b h 45bDgg w 6b'),
        ('Hand 7', 24, 'm 345b 567b 789b h 456bWw w Ww'),
        ('Hand 8', 12, 'm b222 h c333 d444 b567 b8 w b8'),
        ('Hand 9', 43, 'm 345c h 111222333bWs w Ws'),
        ('Hand 10', 51, 'h d1d1d1d1c2c2c2d2d2d2d2d3d3 w d3 self_draw'),
        ('Hand 11', 8, 'm 234b h 567b345678c3d w d3 self_draw'),
        ]
    for name, points, hand in baseline_hands:
        fragment += P(A(name + (" - %d" % points), href=('/?sit=%s' % hand)))

    fragment += A(H2("Input format"), name="format")
    fragment += H3('The tiles') + \
                DL(
                   DT('Bamboos') + DD('1b to 9b') +
                   DT('Characters') + DD('1c to 9c') +
                   DT('Dots') + DD('1d to 9d') + 
                   DT('Winds') + DD('We, Ws, Ww and Wn (East, South, West and North)') +
                   DT('Dragons') + DD('Dr, Dg and Dw (Red, Green and White)') +
                   DT('Flower and Seasons') + DD('F1 to F8')
                  )
    fragment += H3('The tile groups') + \
                DL(
                   DT('h') + DD("Hand - The tiles in the player's hand, just before the hu)") +
                   DT('w') + DD("Winning tile") +
                   DT('c') + DD("Concealed (for concealed kongs)") +
                   DT('m') + DD("Melded sets (for melded chows, pungs and kongs)") +
                   DT('f') + DD("Flowers (for revealed flowers and seasons)") +
                   DT('v') + DD("Visible tiles in discard piles and other players melded sets (used to deduce Last Tile)") +
                   DT('rw') + DD("Round wind") +
                   DT('sw') + DD("Seat wind")
                  )
        
    fragment += H3('Modifiers') + \
                DL(
                   DT('self_draw') + DD("The winning tile was self drawn") +
                   DT('last_turn') + DD("Winning on the last turn (used to deduce Last Tile Draw and Last Tile Claim)") +
                   DT('kong_replacement') + DD("Winning on a replacement tile") +
                   DT('robbing') + DD("Winning by Robbing the Kong") 
                  )

    return fragment

def get_page(situation):
    bgcolor = '#99aaee'
    title = 'MCR Mahjong Hand Score Calculator'
    head = HEAD(TITLE(title))
    header = P(H1(title))
    footer = P(TEXT('This page use ') + A('pyMCR', href='https://github.com/offe/py-mcr') + TEXT(', an open source Mahjong Competition Rules hand scoring library. Post feedback or questions on the ') + A('Swedish Mahjong Association forums', href='https://www.svenskmahjong.se/forum/') + TEXT('.')) + \
    P(TEXT('Tile graphics are from ') + A('Mahjong Wiki', href='http://mahjong.wikidot.com/') + TEXT(' and they are released under a Creative Commons licence.')) + \
    P(TEXT('Version 1.2'))
    if situation == None:
        page = head + BODY(header + help_fragment() + footer, 
                           bgcolor=bgcolor)
    else:
        in_string = situation
        answer_div = mahtml.getAnswerOrError(in_string)
        page = head + BODY(header + get_hand_form(in_string) + 
                           answer_div + footer,  
                           bgcolor=bgcolor)
    return page

def main():
    from BaseHTTPServer import HTTPServer
    from BaseHTTPServer import BaseHTTPRequestHandler
    class myHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if re.match("/images/[bcdWDF][123456789eswnrgw]\.png", self.path):
                self.send_response(200)
                self.send_header('Content-Type', 'image/png')
                self.send_header('Cache-Control', 'max-age=86400, must-revalidate')
                self.end_headers()
                from os import curdir, sep
                filename = curdir + sep + self.path
                print filename
                f = open(curdir + sep + self.path, 'rb')
                self.wfile.write(f.read())
                f.close()
            else:
                self.printCustomTextHTTPResponse(200)
                query_string = urllib.unquote_plus(self.path)
                path, query = urllib.splitquery(query_string)
                print query_string, path, query
                parameters = dict(urllib.splitvalue(v) for v in query.split("&")) if query else {}
                print parameters
    
                if 'sit' in parameters:
                    situation = parameters['sit']
                else:
                    situation = None
                #else:
                    #situation = query_string[1:]
                print "situation:", situation
                page = get_page(situation)
                self.wfile.write('<html>')
                self.wfile.write(page)
                self.wfile.write('</html>')
    
        def printBrowserHeaders(self):
            headers = self.headers.dict
            self.wfile.write("\n<ul>")
            for key, value in headers.items():
                self.wfile.write("\n<li><b>" + key + "</b>: ")
                self.wfile.write(value + "\n</li>\n")
            self.wfile.write("</ul>\n")
    
        def printCustomTextHTTPResponse(self, respcode):
            self.send_response(respcode)
            self.send_header("Content-Type", "text/html")
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
    
        def log_request(self, code='-', size='-'):
            user_agent = self.headers.dict['user-agent']
            self.log_message('"%s" %s %s %s',
                             self.requestline, str(code), str(size), user_agent)

    try:
        port = 8080
        server = HTTPServer(('', port), myHandler)
        print 'Browse to http://localhost:%d/' % port
        while True:
            server.handle_request()
        #server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

# Even shorter:
"""
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write( "hello" )

    @staticmethod
    def serve_forever(port):
        HTTPServer(('', port), MyServer).serve_forever()

if __name__ == "__main__":
    MyServer.serve_forever(8080)

"""


