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

        # Title detect
        title = "MARKET VIEW"
        if "ZERO HERO" in text:
            title = "ZERO HERO"
        elif "BTST" in text:
            title = "BTST VIEW"
        elif "WAIT FOR LEVEL" in text:
            title = "WAIT FOR LEVEL"

        # Strike detect
        strike = re.search(r'(NIFTY50|NIFTY|BANKNIFTY)\s+\d+\s?(PE|CE)', text)

        # Entry detect
        above = re.search(r'ABOVE\s*(\d+)|-\s*(\d+)\+', text)

        # Target detect
        target = re.search(r'TARGET[-\s]*(\d+(?:/\d+)*)', text)

        # SL detect
        sl = re.search(r'SL[-\s]*(\d+)', text)

        strike_text = strike.group(0).title() if strike else ""
        above_text = above.group(1) or above.group(2) if above else ""
        target_text = target.group(1) if target else ""
        sl_text = sl.group(1) if sl else ""

        # fallback target
        if not target_text:
            loose_target = re.search(r'(\d+(?:/\d+)+)\+*', text)
            target_text = loose_target.group(1) if loose_target else ""

        # Final output
        final = f"📌 {title}\n\nStrike: {strike_text}\n\nActive Zone: Above {above_text}\n\nPossible Move: {target_text}\n\nWeakness Below: {sl_text}"

        # Send message
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={
                "chat_id": CHANNEL,
                "text": final
            }
        )

        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot running successfully")
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
