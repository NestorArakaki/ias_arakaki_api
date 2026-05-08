import os
from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Nestor", "email": "nestor@example.com"}
]


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "env": os.getenv("ENV", "local")
    })


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "name and email required"}), 400

    new_user = {
        "id": len(users) + 1,
        "name": data["name"],
        "email": data["email"]
    }

    users.append(new_user)
    return jsonify(new_user), 201

#cambio de prueba 


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    for user in users:
        if user["id"] == user_id:
            return jsonify(user)

    return jsonify({"error": "not found"}), 404


if __name__ == "__main__":
    app.run()