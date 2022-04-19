from http.server import BaseHTTPRequestHandler, HTTPServer


class World:
    has_started = False


router = {}

def setup_idle_router():
    router["/"] = ep_idle_index
    router["/start"] = ep_start
    router["/stop"] = ep_idle_index

def setup_active_router():
    router["/"] = ep_active_index
    router["/start"] = ep_active_index
    router["/stop"] = ep_stop

def ep_idle_index(req):
    req.send_response(200, "OK")
    req.end_headers()
    req.wfile.write(b"World is not started\n")

def ep_active_index(req):
    req.send_response(200, "OK")
    req.end_headers()
    req.wfile.write(b"World has started\n")

def ep_start(req):
    World.has_started = True
    req.send_response(303, "Let's go")
    req.send_header("Location", "/")
    req.end_headers()
    setup_active_router()

def ep_stop(req):
    World.has_started = False
    req.send_response(303, "Let's go")
    req.send_header("Location", "/")
    req.end_headers()
    setup_idle_router()


setup_idle_router()


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        router[self.path](self)


class Server(HTTPServer):

    def service_actions(self):
        print("has_started", World.has_started)


Server(("", 8000), HTTPRequestHandler).serve_forever(poll_interval=2)
