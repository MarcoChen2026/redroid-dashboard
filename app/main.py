import os
import tornado.ioloop
import tornado.web
import tornado.httpserver
import docker
import json

# Docker 客户端初始化
client = docker.from_env()

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class ContainersHandler(tornado.web.RequestHandler):
    def get(self):
        containers = client.containers.list(all=True)
        container_info = []
        for container in containers:
            container_info.append({
                'id': container.id,
                'name': container.name,
                'status': container.status,
                'image': container.image.tags[0] if container.image.tags else 'N/A'
            })
        self.write(json.dumps(container_info))

class StartContainerHandler(tornado.web.RequestHandler):
    def post(self, container_id):
        try:
            container = client.containers.get(container_id)
            container.start()
            self.write(json.dumps({'status': 'success', 'message': f'Container {container_id} started successfully.'}))
        except docker.errors.NotFound:
            self.write(json.dumps({'status': 'error', 'message': 'Container not found.'}))
            self.set_status(404)

class StopContainerHandler(tornado.web.RequestHandler):
    def post(self, container_id):
        try:
            container = client.containers.get(container_id)
            container.stop()
            self.write(json.dumps({'status': 'success', 'message': f'Container {container_id} stopped successfully.'}))
        except docker.errors.NotFound:
            self.write(json.dumps({'status': 'error', 'message': 'Container not found.'}))
            self.set_status(404)

class RestartContainerHandler(tornado.web.RequestHandler):
    def post(self, container_id):
        try:
            container = client.containers.get(container_id)
            container.restart()
            self.write(json.dumps({'status': 'success', 'message': f'Container {container_id} restarted successfully.'}))
        except docker.errors.NotFound:
            self.write(json.dumps({'status': 'error', 'message': 'Container not found.'}))
            self.set_status(404)

def make_app():
    return tornado.web.Application([
        (r"/", IndexHandler),
        (r"/containers", ContainersHandler),
        (r"/container/start/(.*)", StartContainerHandler),
        (r"/container/stop/(.*)", StopContainerHandler),
        (r"/container/restart/(.*)", RestartContainerHandler),
      ], template_path=os.path.join(os.path.dirname(__file__), "templates"))

if __name__ == "__main__":
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(5000)
    tornado.ioloop.IOLoop.current().start()



