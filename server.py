import http.server
import os
import re

class RangeHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()
        
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(404, "File not found")
            return None
        
        range_header = self.headers.get('Range')
        if not range_header or not range_header.startswith('bytes='):
            self.send_response(200)
            self.send_header("Content-type", self.guess_type(path))
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()
            return f
        
        fs = os.fstat(f.fileno())
        file_size = fs[6]
        
        m = re.match(r'bytes=(\d+)-(\d+)?', range_header)
        if not m:
            self.send_error(416, "Requested Range Not Satisfiable")
            f.close()
            return None
        
        start = int(m.group(1))
        end = int(m.group(2)) if m.group(2) else file_size - 1
        if start >= file_size or end >= file_size:
            self.send_error(416, "Requested Range Not Satisfiable")
            f.close()
            return None
        
        length = end - start + 1
        self.send_response(206)
        self.send_header("Content-type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
        self.send_header("Content-Length", str(length))
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()
        
        f.seek(start)
        return f

if __name__ == '__main__':
    http.server.test(HandlerClass=RangeHTTPRequestHandler, port=8000)
