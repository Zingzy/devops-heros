import json
import sys
from urllib.request import urlopen

base_url, expected_version = sys.argv[1], sys.argv[2]

with urlopen(f"{base_url}/healthz", timeout=5) as resp:
    health = json.load(resp)
print("GET /healthz ->", health)
assert health["status"] == "ok"
assert health["version"] == expected_version, f"running {health['version']}, expected {expected_version}"

with urlopen(f"{base_url}/calc/add?a=10&b=5", timeout=5) as resp:
    calc = json.load(resp)
print("GET /calc/add?a=10&b=5 ->", calc)
assert calc["result"] == 15

print("Smoke test passed")
