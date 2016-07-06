# simple_web_server.py

import SimpleHTTPServer
import SocketServer
import cgi
import HTTP

###################################################################################################
def main():
    myRequestHandler = MyRequestHandler
    socketTCPServer = SocketServer.TCPServer(('0.0.0.0', 8080), myRequestHandler)
    print 'starting server, use <Ctrl-C> to stop'
    socketTCPServer.serve_forever()

###################################################################################################
class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        print "in do_GET(self)"
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        print "in do_POST(self)"        # this shows successfully to the command line

        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}

        print postvars

        form = cgi.FieldStorage()

        print cgi.print_form(form)      # this always prints an empty form

        print str(form.getvalue('name'))        # this always prints an empty string

        if "name" not in form or "addr" not in form:        # the if never runs
            print "Please fill in the name and addr fields."
        else:
            print "<p>name:", form["name"].value
            print "<p>addr:", form["addr"].value

        self.wfile.write("test response 123 \n")    # this shows successfully in Postman
        self.send_response(200)                     # the 200 is successfully received by Postman

###################################################################################################
if __name__ == "__main__":
    main()

