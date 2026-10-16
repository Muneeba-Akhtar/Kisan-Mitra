
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

HOST = "127.0.0.1"
PORT = 5000


def get_guidance(crop, question):
    q = question.lower()
    crop = crop or "your crop"

    if any(word in q for word in ["yellow", "yellowing", "पीला", "पीली"]):
        return (
            f"🌱 Possible issue: Yellowing leaves in {crop} can have "
            "several causes, including nutrient deficiency, excess water, "
            "or pests. Check soil moisture and inspect both sides of the "
            "leaves. Avoid applying fertilizer or pesticides until the "
            "cause is clearer."
        )

    if any(word in q for word in ["water", "irrigation", "पानी", "सिंचाई"]):
        return (
            f"💧 For {crop}, check soil moisture before irrigating. "
            "Avoid waterlogging and consider the crop's growth stage, "
            "recent rainfall, and soil type before deciding when to water."
        )

    if any(word in q for word in ["pest", "insect", "कीट", "कीड़ा"]):
        return (
            f"🔎 For pests in {crop}, inspect the leaves, stems, and "
            "undersides of leaves. Take a clear photo and identify the "
            "pest before choosing a treatment. Ask your local KVK "
            "agriculture expert before applying pesticides."
        )

    if any(word in q for word in ["mango", "आम", "fruit", "फल"]):
        return (
            "🥭 For mango trees, inspect leaves, flowers, and fruits for "
            "visible symptoms. Orchard advice depends on the growth stage, "
            "weather, and symptoms. Share a photo or consult a local "
            "agriculture expert for a more specific recommendation."
        )

    return (
        f"🌾 Kisan Mitra farming guidance for {crop}: "
        "First, inspect the crop for visible symptoms and check soil "
        "moisture and recent weather conditions. Avoid guessing pesticide "
        "doses. Tell us when the problem started, which crop stage it is "
        "in, and what symptoms you observe for more targeted guidance. "
        "You can also consult your local Krishi Vigyan Kendra (KVK)."
    )



def get_lucknow_weather():
    from urllib.request import urlopen
    from urllib.parse import urlencode

    params = urlencode({
        "latitude": 26.8467,
        "longitude": 80.9462,
        "current": "temperature_2m,relative_humidity_2m,precipitation,rain,wind_speed_10m",
        "timezone": "Asia/Kolkata"
    })

    try:
        url = "https://api.open-meteo.com/v1/forecast?" + params

        with urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))

        current = data.get("current", {})

        return {
            "available": True,
            "location": "Lucknow",
            "temperature_c": current.get("temperature_2m"),
            "humidity_percent": current.get("relative_humidity_2m"),
            "rain_mm": current.get("rain"),
            "precipitation_mm": current.get("precipitation"),
            "wind_speed_kmh": current.get("wind_speed_10m"),
            "time": current.get("time")
        }

    except Exception as error:
        print("WEATHER ERROR:", error)
        return {
            "available": False,
            "location": "Lucknow",
            "message": "Live weather is temporarily unavailable."
        }

class KisanMitraHandler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_json({"success": True})

    
    
    
    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/")
        print("REQUESTED PATH:", repr(path))

        if path == "":
            self.send_json({
                "status": "online",
                "project": "Kisan Mitra",
                "message": "Kisan Mitra backend is running!"
            })
        elif path == "/weather":
            self.send_json(get_lucknow_weather())
        else:
            self.send_json({
                "success": False,
                "error": "Route not found",
                "path_received": path
            }, 404)



    def do_POST(self):
        if self.path != "/get-guidance":
            self.send_json({"success": False, "error": "Route not found"}, 404)
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length).decode("utf-8"))

            question = str(data.get("question", "")).strip()
            crop = str(data.get("crop", "your crop"))

            if not question:
                self.send_json({
                    "success": False,
                    "error": "Please enter a farming question."
                }, 400)
                return

            
            weather = get_lucknow_weather()

            answer = get_guidance(crop, question)

            if weather.get("available"):
                weather_note = (
                    f"\n\n🌦️ Current Lucknow weather: "
                    f"{weather['temperature_c']}°C, "
                    f"humidity {weather['humidity_percent']}%, "
                    f"rainfall {weather['precipitation_mm']} mm, "
                    f"wind {weather['wind_speed_kmh']} km/h."
                )
                answer += weather_note

            self.send_json({
                "success": True,
                "answer": answer,
                "crop": crop,
                "mode": "demo"
            })

        except Exception:
            self.send_json({
                "success": False,
                "error": "Could not process your question. Please try again."
            }, 400)

    def log_message(self, format, *args):
        print("[Kisan Mitra]", format % args)


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), KisanMitraHandler)
    print("\n🌱 KISAN MITRA IS RUNNING!")
    print("Open http://127.0.0.1:5000/ to test the backend.")
    print("Keep this terminal open while using your website.")
    print("Press Ctrl+C to stop.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKisan Mitra server stopped.")
        server.server_close()
