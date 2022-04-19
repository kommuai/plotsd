import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from tick import World, tick


router = {}


def setup_idle_router():
    router["/"] = ep_idle_index
    router["/start"] = ep_start
    router["/stop"] = ep_idle_index
    router["/view"] = ep_view

def setup_active_router():
    router["/"] = ep_active_index
    router["/start"] = ep_active_index
    router["/stop"] = ep_stop
    router["/view"] = None

def ep_static(req):
    req.File("/".join(["statics"] + req.path.split("/")[2:]))

def ep_idle_index(req):
    req.File("views/idle_index.html")

def ep_active_index(req):
    req.File("views/active_index.html")

def ep_view(req):
    req.send_response(200, "OK")
    req.send_header("Content-Type", "application/json")
    req.end_headers()
    req.wfile.write(bytes(json.dumps(World.data), encoding='utf8'))

def ep_start(req):
    World.start()
    setup_active_router()
    req.Redirect("/")

def ep_stop(req):
    World.stop()
    setup_idle_router()
    req.Redirect("/view")


setup_idle_router()


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def File(self, filename):
        self.send_response(200, "OK")
        self.end_headers()
        with open(filename, "rb") as f:
            self.wfile.write(f.read())

    def Redirect(self, path):
        self.send_response(303, "Let's go")
        self.send_header("Location", path)
        self.end_headers()

    def do_GET(self):
        try:
            router[self.path](self)
        except KeyError:
            # Handle static files
            if self.path.startswith("/s"):
                ep_static(self)
            else:
                self.send_response(404, "Nope")
                self.end_headers()


class Server(HTTPServer):

    def service_actions(self):
        tick()


Server(("", 8000), HTTPRequestHandler).serve_forever(poll_interval=2)
