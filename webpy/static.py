#
# System includes
#
import cgi
import web
import os


class static_handler:
    '''
    This class is called when NO MATCH IS FOUND in the mapping that is passed to the webpy
    application (urls parameter in index.py).
    '''    
    def GET(self, path):
        '''
        @parameter path: The path that was requested by the user, and was forwarded here by index.py
        @return: The contents of a static file.
        '''
        full_path = os.path.join( os.getcwd() , path )

        #
        #   Path traversal protection
        #
        if not full_path.startswith( os.getcwd() ):
            return web.notfound("Sorry, the page you were looking for was not found.")
        
        if os.path.exists( full_path ) and os.path.isfile( full_path ):
            if os.access( full_path, os.R_OK ):
                fh = file( full_path, 'r')
                if full_path.endswith('.css'):
                    web.header('content-type','text/css')
                return fh.read()
            else:
                #
                #   The user has no privileges to read this file
                #
                return web.notfound("Sorry, the file you are trying to access can not be read.")
            
        return web.notfound("Sorry, the page you were looking for was not found.")
