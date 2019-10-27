import webapp2
import mahjongserver
import logging

class MainPage(webapp2.RequestHandler):
    def get(self):
        situation_string = self.request.get('sit', None)
        if situation_string:
            situation_string = str(situation_string)
        logging.info(situation_string)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(mahjongserver.get_page(situation_string))

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

"""
import cgi
import os
import mahjongserver
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):
    def get(self):
        situation_string = self.request.get('sit', None)
        if situation_string:
            situation_string = str(situation_string)
        logging.info(situation_string)
        template_values = {
          'page': mahjongserver.get_page(situation_string),
        }

        path = os.path.join(os.path.dirname(__file__), 'template.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('.*', MainPage)], debug = True)

def main():
	run_wsgi_app(application)
	
if __name__ == "__main__":
	main()
"""