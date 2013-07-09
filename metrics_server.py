#!/usr/bin/python 
import time
import BaseHTTPServer
from cgi import parse_multipart, parse_header, parse_qs
from metrics_storer import writeToDir, mapValues, readDirAsJson, toCsv

HOST_NAME = 'localhost' #'team-metrics.isg.deere.com' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9000 # Maybe set this to 9000.

def getFirstOf(i):
    o = dict()
    for k,v in i.items():
        if len(v) >= 1:
            o[k] = v[0]
        else:
            o[k] = ''
    return o

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        """Respond to a GET request."""
        if s.path == '/csv':
            s.send_response(200)
            s.send_header('Content-Disposition', 'attachment; filename="team_metrics.csv"')
            s.end_headers()
            data = readDirAsJson("data")
            toCsv(s.wfile, data)
        else:
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            with open("index.html") as f:
                html = f.read()
                s.wfile.write(html)
        

    def parse_POST(s):
        postvars = {}
        ctype, pdict = parse_header(s.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(s.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(s.headers['content-length'])
            content = s.rfile.read(length)
            postvars = parse_qs(content, keep_blank_values=1)
        return postvars
    
    def do_POST(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        postdata = s.parse_POST()
        writeToDir('data', mapValues(postdata))
        s.wfile.write("<html><head><title>Thanks</title></head><body>Thank you</body></html>")

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
