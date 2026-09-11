import os
from flask import Flask, jsonify

app = Flask(__name__)

# Service metadata
APP_VERSION = "1.0.0-rc1"


@app.route("/environment", methods=["GET"])
def environment():
    current_env = os.environ.get("APP_ENV", "development")
    return jsonify({"environment": current_env}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
