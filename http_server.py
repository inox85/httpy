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
#broker_address="iot.eclipse.org" #use external broker
import cgi




class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = """
                <html>
                <head>
                <title>Control Centre  </title>
                </head>
                <body>
                <font size="20"> </font>
                <p> <font size="20">  <b>Control  Centre</b> </font>  </p>
                </body>

                <form action="/" method="POST">
                    <input type="submit" name="submit" value="1">
                    <input type="submit" name="submit" value="0">
                </form>

                <form action="https://google.com">
                    <input type="submit" value="Go to Google" />
                </form>

                <p> <button type="submit1">LED 1</button> </p>
                <p> <button type="submit2">LED 2</button> </p>
                <p> <button type="submit3">LED 3</button> </p>
                <p> <button type="submit4">LED 4</button> </p>
                <p> <button type="submit5">LED 5</button> </p>
                <p> <button type="submit6">LED 6</button> </p>
                <p> <button type="submit7">BUZZER</button> </p>
                </html>
                """
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._html("hi!"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length'])    # Get the size of data
        print(content_length)
        post_data = self.rfile.read(content_length).decode("utf-8")   # Get the data
        print(post_data)
        post_data = post_data.split("=")[1]    # Only keep the value
        print(post_data)
        self._set_headers()
        self.wfile.write(self._html("POST!"))
        client = mqtt.Client("P1") #create new instance
        client.connect(broker_address) #connect to broker
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
        default="localhost",
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
    run(addr=args.listen, port=args.port)