import json
import os
import random
import resource
import secrets
import threading
import time
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", "8000"))
OTLP_URL = os.environ.get("OTLP_TRACES_URL", "")
START_TIME = time.time()

lock = threading.Lock()
requests_total = {}
duration_sum = 0.0
duration_count = 0
healthy = True


def log(level, msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"{ts} {level} {msg}", flush=True)


def export_trace(spans):
    if not OTLP_URL:
        return
    body = {
        "resourceSpans": [{
            "resource": {"attributes": [
                {"key": "service.name", "value": {"stringValue": "demo-app"}}]},
            "scopeSpans": [{"scope": {"name": "demo-app"}, "spans": spans}],
        }]
    }
    req = urllib.request.Request(
        OTLP_URL, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=2).read()
    except Exception as e:
        log("WARN", f"trace export failed: {e}")


def span(trace_id, span_id, parent, name, start, end, attrs):
    return {
        "traceId": trace_id, "spanId": span_id, "parentSpanId": parent,
        "name": name, "kind": 2 if not parent else 3,
        "startTimeUnixNano": str(int(start * 1e9)),
        "endTimeUnixNano": str(int(end * 1e9)),
        "attributes": [{"key": k, "value": {"stringValue": str(v)}} for k, v in attrs.items()],
    }


def burn(seconds):
    end = time.time() + seconds
    while time.time() < end:
        pass


def metrics_text():
    usage = resource.getrusage(resource.RUSAGE_SELF)
    with open("/proc/self/statm") as f:
        rss = int(f.read().split()[1]) * os.sysconf("SC_PAGE_SIZE")
    lines = [
        "# HELP demo_http_requests_total HTTP requests handled, by path and status code.",
        "# TYPE demo_http_requests_total counter",
    ]
    with lock:
        for (path, code), n in sorted(requests_total.items()):
            lines.append(f'demo_http_requests_total{{path="{path}",code="{code}"}} {n}')
        lines += [
            "# HELP demo_request_duration_seconds Time spent handling /work requests.",
            "# TYPE demo_request_duration_seconds summary",
            f"demo_request_duration_seconds_sum {duration_sum}",
            f"demo_request_duration_seconds_count {duration_count}",
            "# HELP demo_app_healthy 1 when /health returns 200, 0 when it returns 503.",
            "# TYPE demo_app_healthy gauge",
            f"demo_app_healthy {1 if healthy else 0}",
        ]
    lines += [
        "# HELP process_cpu_seconds_total User and system CPU time used by the app.",
        "# TYPE process_cpu_seconds_total counter",
        f"process_cpu_seconds_total {usage.ru_utime + usage.ru_stime}",
        "# HELP process_resident_memory_bytes Resident memory of the app.",
        "# TYPE process_resident_memory_bytes gauge",
        f"process_resident_memory_bytes {rss}",
        "# HELP process_start_time_seconds Unix time the app started.",
        "# TYPE process_start_time_seconds gauge",
        f"process_start_time_seconds {START_TIME}",
    ]
    return "\n".join(lines) + "\n"


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def reply(self, code, body, ctype="application/json"):
        data = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
        path = self.path.split("?")[0]
        if path != "/metrics":
            with lock:
                requests_total[(path, code)] = requests_total.get((path, code), 0) + 1

    def do_GET(self):
        global healthy, duration_sum, duration_count
        path = self.path.split("?")[0]
        if path == "/metrics":
            self.reply(200, metrics_text(), "text/plain; version=0.0.4")
        elif path == "/health":
            if healthy:
                self.reply(200, '{"status":"ok"}')
            else:
                self.reply(503, '{"status":"unhealthy"}')
                log("ERROR", "health check failed, returning 503")
        elif path == "/work":
            trace_id, root_id, db_id = secrets.token_hex(16), secrets.token_hex(8), secrets.token_hex(8)
            start = time.time()
            time.sleep(random.uniform(0.01, 0.05))
            db_start = time.time()
            time.sleep(random.uniform(0.05, 0.3))
            db_end = time.time()
            end = time.time()
            with lock:
                duration_sum += end - start
                duration_count += 1
            self.reply(200, json.dumps({"result": "done", "trace_id": trace_id}))
            log("INFO", f"GET /work 200 {end - start:.3f}s db={db_end - db_start:.3f}s trace_id={trace_id}")
            threading.Thread(target=export_trace, args=([
                span(trace_id, root_id, "", "GET /work", start, end, {"http.method": "GET", "http.route": "/work"}),
                span(trace_id, db_id, root_id, "SELECT orders", db_start, db_end, {"db.system": "postgresql"}),
            ],), daemon=True).start()
        elif path == "/burn":
            seconds = int(self.path.split("seconds=")[-1]) if "seconds=" in self.path else 60
            threading.Thread(target=burn, args=(seconds,), daemon=True).start()
            self.reply(200, json.dumps({"burning_cpu_for": seconds}))
            log("WARN", f"burning one CPU core for {seconds}s")
        elif path == "/admin/fail":
            healthy = False
            self.reply(200, '{"healthy":false}')
            log("WARN", "health switched to FAILING")
        elif path == "/admin/recover":
            healthy = True
            self.reply(200, '{"healthy":true}')
            log("INFO", "health switched to OK")
        elif path == "/":
            self.reply(200, '{"app":"demo-app"}')
        else:
            self.reply(404, '{"error":"not found"}')
            log("WARN", f"GET {path} 404")


if __name__ == "__main__":
    log("INFO", f"demo-app listening on :{PORT}")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
