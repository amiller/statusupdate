#!/home/soc1024c/bin/python
# -*- coding: utf-8 -*-

import web
from static import static_handler
from django.conf import settings
settings.configure(TEMPLATE_DIRS=('.'))
from django.template.loader import render_to_string

urls = ("/", "render",
        "/(.*)", "static_handler")
app = web.application(urls, globals())

class render:
    def GET(self):
        # Check for the key in the query
        key = None
        if not key:
            # generate a fresh key and redirect
            pass

        # Look up our state from the database
        state = None

        from webpy import make_status
        statuses = [(make_status.random_template(),
                     make_status.random_person())
                    for _ in range(6)]

        

        web.header('content-type', 'text/html')
        return unicode(render_to_string('jetz.html', locals()))


if __name__ == "__main__":
    app.internalerror = web.debugerror 
    app.run()
