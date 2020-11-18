#!/usr/bin/env python
"""
Very simple HTTP server in python (Updated for Python 3.7)
Usage:
    ./dummy-web-server.py -h
    ./dummy-web-server.py -l localhost -p 8000
Send a GET request:
    curl http://localhost:8000
Send a HEAD request:
    curl -I http://localhost:8000
Send a POST request:
    curl -d "foo=bar&bin=baz" http://localhost:8000
"""
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import paho.mqtt.client as mqtt #import the client1
import time
broker_address="inoxhome.duckdns.org"
#broker_address="151.40.232.173"
#broker_address="iot.eclipse.org" #use external broker
import cgi
from queue import Queue
import threading
import datetime

q=Queue()



def on_message(client1, userdata, message):
    #global messages
    m="message received  "  ,str(message.payload.decode("utf-8"))
    messages.append(m)#put messages in list
    q.put(m) #put messages on queue
    print("message received  ",m)


class S(BaseHTTPRequestHandler):
    
    date = datetime.datetime.now()
    
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
        self._set_headers()
        self.wfile.write(self._html("hi!"))

    def do_HEAD(self):
        self._set_headers()
        
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length'])    # Get the size of data
        post_data = self.rfile.read(content_length).decode("utf-8")   # Get the data
        post_data = post_data.split("=")[1]    # Only keep the value
        self._set_headers()
        self.wfile.write(self._html("POST!"))
        print("Pubblico su inTopic")
        client.publish("inTopic",post_data)#publish
        
def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8081):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="192.168.1.45",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    client = mqtt.Client("server_http") #create new instance
    client.connect(broker_address) #connect to broker
    run(addr=args.listen, port=args.port)




