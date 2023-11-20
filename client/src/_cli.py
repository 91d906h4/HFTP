# Import modules.
import sys

def cli() -> dict:
    params = {
        "host": "127.0.0.1",
        "port": 22
    }

    for param in sys.argv[1:]:
        if param.startswith("--host="):
            params["host"] = param[7:]
        elif param.startswith("--port="):
            params["port"] = int(param[7:])

    return params