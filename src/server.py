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

def ep_static(req):
    req.File("/".join(["statics"] + req.path.split("/")[2:]))

def ep_idle_index(req):
    req.File("views/idle_index.html")

def ep_active_index(req):
    req.File("views/active_index.html")

def ep_start(req):
    World.has_started = True
    setup_active_router()
    req.Redirect("/")

def ep_stop(req):
    World.has_started = False
    setup_idle_router()
    req.Redirect("/")


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


def tick():
    print("has_started", World.has_started)

class Server(HTTPServer):

    def service_actions(self):
        tick()


Server(("", 8000), HTTPRequestHandler).serve_forever(poll_interval=2)
