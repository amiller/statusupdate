#!/home/soc1024c/bin/python
# -*- coding: utf-8 -*-

import web

urls = ("/.*", "hello")
app = web.application(urls, globals())

class hello:
    def GET(self):
        import make_status
        #web.header('Content-Type', 'text/plain')
        return make_status.random_template()

if __name__ == "__main__":
    app.internalerror = web.debugerror 
    app.run()
