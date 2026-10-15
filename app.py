from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=None)

@app.get("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")

@app.get("/<path:filename>")
def files(filename):
    # Serve project assets if any are added later.
    return send_from_directory(BASE_DIR, filename)

@app.post("/api/advice")
def advice():
    payload = request.get_json(silent=True) or {}
    crop = str(payload.get("crop", "Other"))[:80]
    question = str(payload.get("question", "")).strip()[:2000]
    stage = str(payload.get("stage", "Not sure"))[:100]
    if not question:
        return jsonify({"error": "Please describe the crop problem."}), 400

    text = question.lower()
    title = "Start with careful observation"
    intro = "Crop symptoms can have several causes. Check the affected area and how quickly symptoms are spreading before choosing a treatment."
    steps = [
        "Inspect a few affected and healthy plants and note the pattern of symptoms.",
        "Take clear photos of the whole plant and close-ups of the affected part.",
        "Avoid mixing or applying pesticides until the cause is identified.",
        "Ask your local Krishi Vigyan Kendra (KVK) or agriculture officer to confirm the diagnosis before treatment.",
    ]

    if re.search(r"कीड़ा|कीड़े|insect|worm|pest|bug|बौर", text):
        title = f"Possible pest issue on {crop}"
        intro = "A pest may be involved, but the exact insect needs to be identified before selecting a control method."
        steps = [
            "Check whether insects, eggs, webbing, holes, or sticky residue are visible.",
            "Photograph the affected part and one healthy part for comparison.",
            "Avoid spraying during strong wind and do not mix products without expert advice.",
            "Share the photos with your nearest KVK or agriculture officer for a crop-specific recommendation.",
        ]
    elif re.search(r"पीला|yellow|spots|धब्ब|सूख|dry|wilting|मुरझ|रोग|fungus|फफूंद", text):
        title = "Possible leaf or plant health issue"
        intro = "Yellowing, spots, or wilting can be caused by disease, water stress, nutrition, or pests. The pattern matters."
        steps = [
            "Check whether symptoms appear on old leaves, new leaves, or the whole plant.",
            "Check soil moisture and whether water is collecting around roots.",
            "Look under leaves for insects and note whether spots are spreading.",
            "Get a diagnosis from a local agricultural expert before applying a treatment.",
        ]
    elif re.search(r"बारिश|rain|weather|मौसम|पानी|water|irrigat", text):
        title = "Plan farm work with weather in mind"
        intro = "Weather-sensitive farm operations should be planned using a reliable local forecast and the crop’s current stage."
        steps = [
            "Check the latest local forecast before irrigation or spraying.",
            "Avoid spraying when rain is expected soon or wind conditions are unsafe; follow the product label.",
            "Do not irrigate waterlogged fields; check soil moisture first.",
            "This prototype does not fetch live weather, so confirm conditions using an official forecast.",
        ]

    if crop == "Mango" and re.search(r"बौर|flower|blossom", text):
        intro = "Mango flowering can be affected by several insects and diseases. Identify the pest or symptom first; a generic spray recommendation could harm pollinators or the crop."

    return jsonify({"title": title, "intro": intro, "steps": steps, "stage": stage, "mode": "backend"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
