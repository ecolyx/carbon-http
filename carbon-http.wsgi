#!/usr/bin/env python

#from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
import socket
import sys
import time

#html = """
#<html>
#<body>
#   <p>
#        Metric: %(metric)s<br>
#        Details: %(metricvalue)s %(metrictime)s
#    </p>
#</body>
#</html>
#"""

def application (environ, start_response):

    # Returns a dictionary in which the values are lists
    d = parse_qs(environ['QUERY_STRING'])

    # As there can be more than one value for a variable then
    # a list is provided as a default value.
    metric = d.get('metric', [''])[0] # Returns the first metric
    metricvalue = d.get('value', [''])[0] # Returns first metric value
    metrictime = d.get('ts', [''])[0] # Returns first metric timestamp

    # Always escape user input to avoid script injection
    metric = escape(metric)
    metricvalue = escape(metricvalue)
    metrictime = escape(metrictime)
    if not metrictime:
        metrictime = str(int(time.time()))

    # Create a TCP/IP socket
    sock = socket.socket()

    # Connect the socket to the port where the server is listening
    sock.connect(('localhost', 2003))

    # Send data
    message = "%s %s %s\n" % (metric, metricvalue, metrictime)
    sock.sendall(message)
    sock.close()

    # prepare and send response
    response_body = "<html><body><p>Metric: \"%s\"<br><p>Value: %s</p><br><p>Time: %s</p></body></html>" % (metric, metricvalue, metrictime)

    status = '200 OK'

    # Now content type is text/html
    response_headers = [('Content-Type', 'text/html'),
                        ('Content-Length', str(len(response_body)))]

    start_response(status, response_headers)
    return [response_body]
