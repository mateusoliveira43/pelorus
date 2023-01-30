from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Tuple


def read_file() -> Tuple[bytes, str]:
    with open(Path(__file__).resolve().parent / "response.txt", "br") as file:
        file_bytes = file.read()
    return (file_bytes, file_bytes.decode("utf-8"))


class ResponseHandler(BaseHTTPRequestHandler):
    file_bytes, file_text = read_file()
    print(f"Loaded response.txt with contents {file_text} (as bytes {file_bytes})")

    def do_GET(self) -> None:  # noqa pylint:disable=invalid-name
        self.log_message(
            f"Got request, returning {self.file_text} (as bytes {self.file_bytes})"
        )
        self.send_response(200, "PELORUS IS COOL")
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(self.file_bytes)))
        self.end_headers()

        self.wfile.write(self.file_bytes)


def main() -> None:
    server = HTTPServer(("", 8080), ResponseHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
