import http.server
import threading
import random
import time
import subprocess
import os


# Directory from which to serve files
SERVE_DIR = "./test/testdata/fragments"  # Update this to your serving directory path

# Directory to download files
DOWNLOAD_DIR = "."  # Update this to your download directory path


class FlakyHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SERVE_DIR, **kwargs)

    def do_GET(self):
        current_time = time.time()
        # print("\n\n")
        # print(current_time - start_time)
        # print("\n\n")
        if random.choice([True, False, False]):
            time.sleep(random.uniform(0.5, 1))
        if 5 > current_time - start_time > 3:
            self.send_error(404)
            return
        elif 20 > current_time - start_time > 7:
            self.send_error(404)
            return
        super().do_GET()


def run_server():
    server_address = ("127.0.0.1", 8000)
    httpd = http.server.HTTPServer(server_address, FlakyHTTPHandler)
    httpd.serve_forever()


server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()


def download_with_youtube_dl():
    url = "http://127.0.0.1:8000/test_fragments.m3u8"
    try:
        subprocess.run(
            [
                "python3",
                "-m",
                "youtube_dl",
                "--hls-prefer-native",
                "--retry-delay",
                "200",
                "--abort-on-unavailable-fragment",
                url,
            ],
            check=False,
        )
        print("Download completed successfully.")
    except subprocess.CalledProcessError as e:
        print("youtube-dl failed with error:", e)


time.sleep(1)  # Wait for the server to start
start_time = time.time()
download_with_youtube_dl()
