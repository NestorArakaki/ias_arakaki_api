import os
import psycopg2
from flask import Flask, jsonify, request
from app.db import get_connection, init_db
from app.validators import validate_create_user, validate_update_user

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    try:
        init_db()
        db_status = "ok"
        status_code = 200
    except RuntimeError:
        db_status = "not_configured"
        status_code = 500
    except psycopg2.Error:
        db_status = "error"
        status_code = 500

    return jsonify({
        "status": "ok" if status_code == 200 else "error",
        "env": os.getenv("ENV", "local"),
        "database": db_status
    }), status_code


@app.route("/users", methods=["GET"])
def get_users():
    init_db()
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, email FROM users ORDER BY id;")
            users = [dict(row) for row in cursor.fetchall()]

        return jsonify(users), 200
    finally:
        conn.close()


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    init_db()
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, email FROM users WHERE id = %s;",
                (user_id,)
            )
            user = cursor.fetchone()

        if not user:
            return jsonify({"error": "user not found"}), 404

        return jsonify(dict(user)), 200
    finally:
        conn.close()


@app.route("/users", methods=["POST"])
def create_user():
    init_db()
    data = request.get_json()
    validation_error = validate_create_user(data)

    if validation_error:
        return jsonify({"error": validation_error}), 400

    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (name, email)
                    VALUES (%s, %s)
                    RETURNING id, name, email;
                    """,
                    (data["name"], data["email"])
                )
                new_user = cursor.fetchone()

        return jsonify(dict(new_user)), 201
    except psycopg2.errors.UniqueViolation:
        return jsonify({"error": "email already exists"}), 409
    finally:
        conn.close()

#COMENTARIO DE MODIFICAION

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    init_db()
    data = request.get_json()
    validation_error = validate_update_user(data)

    if validation_error:
        return jsonify({"error": validation_error}), 400

    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, name, email FROM users WHERE id = %s;",
                    (user_id,)
                )
                user = cursor.fetchone()

                if not user:
                    return jsonify({"error": "user not found"}), 404

                updated_name = data.get("name", user["name"])
                updated_email = data.get("email", user["email"])

                cursor.execute(
                    """
                    UPDATE users
                    SET name = %s, email = %s
                    WHERE id = %s
                    RETURNING id, name, email;
                    """,
                    (updated_name, updated_email, user_id)
                )
                updated_user = cursor.fetchone()

        return jsonify(dict(updated_user)), 200
    except psycopg2.errors.UniqueViolation:
        return jsonify({"error": "email already exists"}), 409
    finally:
        conn.close()


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    init_db()
    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM users
                    WHERE id = %s
                    RETURNING id, name, email;
                    """,
                    (user_id,)
                )
                deleted_user = cursor.fetchone()

        if not deleted_user:
            return jsonify({"error": "user not found"}), 404

        return jsonify({
            "message": "user deleted",
            "user": dict(deleted_user)
        }), 200
    finally:
        conn.close()


if __name__ == "__main__":
    app.run()