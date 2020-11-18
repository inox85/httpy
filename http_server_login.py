import http.server
from http.server import SimpleHTTPRequestHandler
import sys
import base64
import datetime

key = ""

class AuthHandler(SimpleHTTPRequestHandler):
    ''' Main class to present webpages and authentication. '''
    def do_HEAD(self):
        print("HEAD")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        print("AUTHHEAD")
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        self.date = datetime.datetime.now()
        content = f"""
                <html>
                <head>
                <title>Control Centre  </title>
                </head>
                <meta http-equiv="refresh" content="5">
                <body>
                <font size="20"> </font>
                <p> <font size="20">  <b>Control  Centre</b> </font>  </p>
                </body>

                <form action="/" method="POST">
		    <p><button type="submit" class="switch" name="accendi" value="1">Accendi LED</button></p>
		    <p><button type="submit" class="switch" name="spegni" value="0">Spegni LED</button></p>
                </form>
		<body><h1>{self.date}</h1></body>
                </html>
                """
                
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        global key
        print(key)
        #print(("admin:password").encode("ascii"))
        print(self.headers.get('Authorization'))
        print('Basic '+ str(key).split("'")[1])
        
        ''' Present frontpage with user authentication. '''
        if self.headers.get('Authorization') == None:
            print("Caso 1")
            self.do_AUTHHEAD()
            self.wfile.write(('no auth header received').encode("ascii"))
            pass
        elif self.headers.get('Authorization') == 'Basic '+ str(key).split("'")[1]: 
       	    print("Caso 2")
            self._set_headers()
            self.wfile.write(self._html("hi!")) 
            pass
        else:
            print("Caso 3")
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.get('Authorization').encode("ascii"))
            self.wfile.write(('not authenticated').encode("ascii"))
            pass

def test(HandlerClass = AuthHandler, ServerClass = http.server.HTTPServer):http.server.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    if len(sys.argv)<3:
        print("usage SimpleAuthServer.py [port] [username:password]")
        sys.exit()
    key = base64.b64encode(("admin:pass").encode("ascii"))
    print(key)
    test()

