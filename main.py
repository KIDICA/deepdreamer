import cherrypy
from web.app import App
import os

if __name__ == '__main__':
    web_root =  os.path.dirname(os.path.abspath(__file__)) + '/web/public'
    print("web-root:", web_root)
    cherrypy.server.socket_port = 3000
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.quickstart(App(), config={
       '/': {
            'tools.staticdir.debug': True,
            'tools.staticdir.on': True,
            'tools.sessions.on': True,
            'tools.staticdir.dir': web_root,
            'tools.staticdir.index' : "index.html"
        }
    })