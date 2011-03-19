#!/home/soc1024c/bin/python
# -*- coding: utf-8 -*-

import web

urls = ("/status", "status")
app = web.application(urls, globals())

class status:
    def GET(self):
        import make_status
        return make_status.random_template()

if __name__ == "__main__":
    app.internalerror = web.debugerror 
    app.run()