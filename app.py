import os
from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, join_room
from flask_cors import CORS
from ai_service import process_audio

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_FOLDER = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__, static_folder=FRONTEND_FOLDER)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")

UPLOAD_FOLDER = "recordings"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

print("🚀 Virtual Court Server Starting...")

# =========================
# Serve Frontend
# =========================
@app.route("/")
def serve_frontend():
    return send_from_directory(FRONTEND_FOLDER, "meeting.html")

# =========================
# Socket Events
# =========================
@socketio.on("join")
def handle_join(data):
    room = data["room"]
    username = data["username"]

    join_room(room)
    print(f"👤 {username} joined room {room}")

# =========================
# Audio Upload
# =========================
@app.route("/upload", methods=["POST"])
def upload_audio():
    room = request.form.get("room")
    file = request.files["audio"]

    if not file:
        return jsonify({"error": "No file"}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    print("⏳ Starting AI processing...")

    socketio.emit("processing", {"message": "Processing..."}, room=room)

    result = process_audio(path)

    socketio.emit("result", result, room=room)

    return jsonify({"status": "done"})

if __name__ == "__main__":
    print("🚀 Server running at http://127.0.0.1:3046")
    socketio.run(app, host="127.0.0.1", port=3046)
