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

        title = ""
        if "ZERO HERO" in text:
            title = "ZERO HERO"
        elif "BTST" in text:
            title = "BTST VIEW"
        elif "WAIT FOR LEVEL" in text:
            title = "WAIT FOR LEVEL"
        else:
            title = "MARKET VIEW"

        strike = re.search(r'(NIFTY50|NIFTY|BANKNIFTY)\s+\d+\s?(PE|CE)', text)
        above = re.search(r'ABOVE\s*(\d+)|-\s*(\d+)\+', text)
        target = re.search(r'TARGET\s*-?\s*([\d/]+)|\n([\d/]+)\+\+', text)
        sl = re.search(r'SL\s*-?\s*(\d+)', text)

        strike_text = strike.group(0) if strike else ""
        above_text = above.group(1) or above.group(2) if above else ""
        target_text = target.group(1) or target.group(2) if target else ""
        sl_text = sl.group(1) if sl else ""

        final = f"""📌 {title}

Strike: {strike_text.title()}

Active Zone: Above {above_text}

Possible Move: {target_text}

Weakness Below: {sl_text}"""

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHANNEL, "text": final}
        )

        self.send_response(200)
        self.end_headers()Weakness Below: {sl_text}"""

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHANNEL, "text": final}
        )

        self.send_response(200)
        self.end_headers()
