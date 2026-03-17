from http.server import BaseHTTPRequestHandler
import json
import requests
import os
import re

TOKEN = os.getenv("TOKEN")
CHANNEL = os.getenv("CHANNEL")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        text = data["message"]["text"].upper()

        strike = re.search(r'(\d+\s?(PE|CE))', text)
        above = re.search(r'ABOVE\s+(\d+)', text)
        target = re.search(r'TARGET\s+([\d/]+)', text)
        sl = re.search(r'SL\s+(\d+)', text)

        strike_text = strike.group(1) if strike else ""
        above_text = above.group(1) if above else ""
        target_text = target.group(1) if target else ""
        sl_text = sl.group(1) if sl else ""

        final = f"📌 {strike_text} | above {above_text} | {target_text} possible | below {sl_text} weak"

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHANNEL, "text": final}
        )

        self.send_response(200)
        self.end_headers()
