from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import random, string

app = Flask(__name__)
CORS(app)

url_map = {}  # short_code -> original_url

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.json
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "URL is required"}), 400

    short_code = generate_short_code()
    while short_code in url_map:
        short_code = generate_short_code()

    url_map[short_code] = original_url
    return jsonify({"short_code": short_code, "short_url": f"http://localhost:5000/{short_code}"})

@app.route("/<short_code>")
def redirect_url(short_code):
    if short_code in url_map:
        return redirect(url_map[short_code])
    return "Short code not found", 404

@app.route("/urls", methods=["GET"])
def list_urls():
    return jsonify(url_map)

if __name__ == "__main__":
    app.run(debug=True)
