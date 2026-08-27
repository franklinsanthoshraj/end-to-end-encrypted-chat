from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os, base64, json

app = FastAPI()

# Store connected clients and keys
clients = {}
keys = {}

# Generate RSA keys for server
server_private_key = rsa.generate_private_key(
    public_exponent=65537, key_size=2048
)
server_public_key = server_private_key.public_key()
server_public_pem = server_public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Function to encrypt using AES
def encrypt_message(message, aes_key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padded_message = message.ljust(16 * ((len(message) // 16) + 1))
    ciphertext = encryptor.update(padded_message.encode()) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode()

# Function to decrypt using AES
def decrypt_message(encrypted_message, aes_key):
    data = base64.b64decode(encrypted_message)
    iv, ciphertext = data[:16], data[16:]
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

@app.websocket("/chat/{client_id}")
async def chat(websocket: WebSocket, client_id: str):
    await websocket.accept()
    clients[client_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if message["type"] == "key_exchange":
                keys[client_id] = server_private_key.decrypt(
                    base64.b64decode(message["key"]),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
            elif message["type"] == "chat":
                recipient = message["to"]
                if recipient in clients and recipient in keys:
                    encrypted_msg = encrypt_message(message["message"], keys[recipient])
                    await clients[recipient].send_json({"from": client_id, "message": encrypted_msg})
    except WebSocketDisconnect:
        del clients[client_id]
        del keys[client_id]
