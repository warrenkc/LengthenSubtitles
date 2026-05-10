import http.server
import socketserver

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # These headers are REQUIRED for FFmpeg.wasm to work
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        super().end_headers()

PORT = 8000

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    print("COOP/COEP headers are enabled. FFmpeg.wasm should work now.")
    print("Open http://localhost:8000/trim-video.htm in your browser.")
    httpd.serve_forever()
