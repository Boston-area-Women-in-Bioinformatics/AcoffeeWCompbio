#!/usr/bin/env python3
"""
Simple HTTP server to preview the RSS feed rendering locally.
Run this and open http://localhost:8000/feed.xml in your browser.
"""

import http.server
import socketserver
import os

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for local testing
        self.send_header('Access-Control-Allow-Origin', '*')
        # Ensure XML files are served with correct content type
        if self.path.endswith('.xml'):
            self.send_header('Content-Type', 'application/xml')
        elif self.path.endswith('.xslt') or self.path.endswith('.xsl'):
            self.send_header('Content-Type', 'application/xslt+xml')
        super().end_headers()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🎙️  A Coffee with CompBio - Preview Server")
        print(f"=" * 50)
        print(f"Server running at: http://localhost:{PORT}")
        print(f"")
        print(f"📻 Preview RSS feed: http://localhost:{PORT}/feed.xml")
        print(f"🌐 Preview website:  http://localhost:{PORT}/")
        print(f"")
        print(f"Press Ctrl+C to stop the server")
        print(f"=" * 50)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")
