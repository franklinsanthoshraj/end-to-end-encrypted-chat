End-to-End Encrypted Chat Application:

A secure real-time chat application that uses client-side end-to-end encryption to protect message confidentiality. The application combines RSA-2048 for secure key exchange and AES-256 for message encryption, while a Python FastAPI backend handles real-time communication through WebSockets.

The server acts only as a message relay and does not have access to the plaintext content of messages.

Overview:

-In modern communication systems, protecting message confidentiality is essential. This project demonstrates how end-to-end encryption can be integrated into a real-time web-based chat application.

-The encryption and decryption processes are performed on the client side. Messages are encrypted before transmission and decrypted only by the intended recipient.

The project combines:

- Client-side cryptography
- Real-time WebSocket communication
- Secure key exchange
- Python backend development
- Network-level security validation


Key Features:

- End-to-end encrypted one-to-one messaging
- RSA-2048 based key exchange
- AES-256 message encryption
- Browser-based encryption using Web Crypto API
- Real-time communication using WebSockets
- Python FastAPI backend
- Client-side key generation and encryption
- Server operates as an encrypted-message relay
- Network traffic validation using Wireshark
- Simple and user-friendly chat interface

System Architecture (Simply):

        Sender
          │
          ▼
   Generate / Manage Keys
          │
          ▼
     AES Encryption
          │
          ▼
   Encrypted Message
          │
          ▼
   WebSocket Connection
          │
          ▼
   ┌─────────────────┐
        FastAPI Server        
        Message Relay         
   └────────┬────────┘
            │
            ▼
   WebSocket Connection
            │
            ▼
    Recipient Browser
            │
            ▼
     AES Decryption
            │
            ▼
       Plaintext

Simple explanation:

The sender encrypts the message before sending it. The encrypted message passes through the FastAPI server using WebSockets. The server only forwards the encrypted data and cannot read the message. The recipient receives the message and decrypts it on their device.