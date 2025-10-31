import random
from flask import Flask, jsonify
from pathlib import Path

def load_quotes():
    with Path("data/quotes.txt").open() as fh:
        return [line.strip() for line in fh if line.strip()]

app = Flask(__name__)

@app.get("/quote")
def quote():
    quotes = load_quotes()
    return jsonify({"quote": random.choice(quotes)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)