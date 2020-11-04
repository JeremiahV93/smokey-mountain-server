from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from users import get_single_user, create_user, delete_user, update_user
from categories import get_category_by_id, get_all_categories
from articles import get_single_article, create_article, delete_article
from categories import get_category_by_id, get_all_categories, delete_category
from articles import get_single_article, create_article

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

            return( resource, key, value )

        else:
            id = None

            try: 
                id = int(path_params[2])
            except IndexError:
                pass
            except ValueError:
                pass

            return( resource, id )

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
            ( resource, id ) = parsed

            if resource == "users":
                if id is not None:
                    response = f"{get_single_user(id)}"
                else:
                    response = ""
            elif resource == "articles":
                if id is not None:
                    response = f"{get_single_article(id)}" 
                else:
                    response = ""
            elif resource == "categories":
                if id is not None:
                    response = f"{get_category_by_id(id)}" 
                else:
                    response = f"{get_all_categories()}"          

        self.wfile.write(response.encode())

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)
      

        if resource == "users":
            new_user = None
            new_user = create_user(post_body)
            self.wfile.write(f"{new_user}".encode())
        elif resource == "articles":
            new_article = None
            new_article = create_article(post_body)
            self.wfile.write(f"{new_article}".encode())

    def do_DELETE(self):
        self._set_headers(204)
        (resource, id) = self.parse_url(self.path)
        if resource == 'users':
                delete_user(id)
        elif resource == 'articles':
                delete_article(id)
        elif resource == 'categories':
            delete_category(id)        
        self.wfile.write("".encode())

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        # Parse the URL
        (resource, id) = self.parse_url(self.path)
        success = False
        if resource == "users":
            success = update_user(id, post_body)
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
        self.wfile.write("".encode())        

def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()
