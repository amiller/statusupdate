#!/home/soc1024c/sandboxes/statusupdate/bin/python
# -*- coding: utf-8 -*-

from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer

import gevent
import web

from static import static_handler
from mako.template import Template
import sys


urls = ("/", "render",
        "/(.*)", "static_handler")

class render:
    def GET(self):
        # Check for the key in the query
        key = None
        if not key:
            # generate a fresh key and redirect
            pass

        # Look up our state from the database
        state = None

        import make_status
        statuses = [(make_status.random_template(),
                     make_status.random_person())
                    for _ in range(6)]


        web.header('content-type', 'text/html')
        template = Template(filename='template_statusupdate.html',
                            input_encoding='utf-8',
                            encoding_errors='replace',
                            output_encoding='utf-8')
        return template.render(statuses=statuses)


if __name__ == "__main__":
    PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8280
    app = web.application(urls, globals())
    app.internalerror = web.debugerror 
    server = WSGIServer(('0.0.0.0', PORT), app.wsgifunc())
    server.serve_forever()
