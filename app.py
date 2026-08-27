from flask import Flask, render_template
from flask_socketio import SocketIO, send
from cryptography.fernet import Fernet

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

# Generate a random encryption key (Use a fixed key for testing)
key = Fernet.generate_key()
cipher = Fernet(key)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("message")
def handle_message(msg):
    print(f"Received message: {msg}")

    # Encrypt the message
    encrypted_msg = cipher.encrypt(msg.encode()).decode()
    send(encrypted_msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)