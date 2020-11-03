from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        if "?" in resource:
            param = resource.split("?")[1] 
            resource = resource.split("?")[0]  
            pair = param.split("=")  
            key = pair[0]  
            value = pair[1]

            return(resource, key, value)

        else:
            id = None

            try: 
                id = int(path_params[2])
            except IndexError:
                pass
            except ValueError:
                pass

            return(resource, id)

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)

        response = {}

        parsed = self.parse_url(self.path)

        if len(parsed) == 2:
            (resource, id) = parsed

            if resource == "users":
                if id is not None:
                    response = f"{get_single_user(id)}"
                else:
                    response = None

def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()
