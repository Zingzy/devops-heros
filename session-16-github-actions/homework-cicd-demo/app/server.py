import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from app.calculator import add, divide, multiply, subtract

OPERATIONS = {"add": add, "subtract": subtract, "multiply": multiply, "divide": divide}
VERSION = os.environ.get("APP_VERSION", "dev")


class CalculatorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/healthz":
            return self.send_json(200, {"status": "ok", "version": VERSION})

        parts = url.path.strip("/").split("/")
        if len(parts) != 2 or parts[0] != "calc" or parts[1] not in OPERATIONS:
            return self.send_json(404, {"error": "use /calc/<add|subtract|multiply|divide>?a=..&b=.."})

        query = parse_qs(url.query)
        try:
            a = float(query["a"][0])
            b = float(query["b"][0])
            result = OPERATIONS[parts[1]](a, b)
        except (KeyError, ValueError) as e:
            return self.send_json(400, {"error": str(e)})
        self.send_json(200, {"op": parts[1], "a": a, "b": b, "result": result, "version": VERSION})

    def send_json(self, status, body):
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def main():
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), CalculatorHandler)
    print(f"Calculator API {VERSION} listening on :{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
