import socket
import threading

class P2PChat:
    def __init__(self, port=12345, broadcast_ip="255.255.255.255"):
        """
        Initialize the peer-to-peer chat system.
        """
        self.port = port  # Port number for communication
        self.broadcast_ip = broadcast_ip  # Broadcast IP to send messages to all peers
        self.running = True  # Control flag to stop the chat safely

        # Create a UDP socket for listening to messages
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.listener.bind(("", self.port))  # Bind to the port to receive messages

        # Create a UDP socket for sending messages
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def listen(self):
        """
        Listen for incoming messages from other peers.
        Runs in a separate thread.
        """
        print("🔹 Listening for incoming messages...")
        while self.running:
            try:
                data, addr = self.listener.recvfrom(1024)  # Receive message (max 1024 bytes)
                print(f"\n📩 {addr[0]}: {data.decode()}")  # Print the message with sender's IP
            except OSError:
                break  # Exit loop if an error occurs (e.g., when stopping the chat)

    def send(self, message):
        """
        Send a message to all peers in the network.
        """
        self.sender.sendto(message.encode(), (self.broadcast_ip, self.port))  # Broadcast message

    def start(self):
        """
        Start the listener thread to receive messages in the background.
        """
        self.listener_thread = threading.Thread(target=self.listen, daemon=True)
        self.listener_thread.start()  # Start listening in a separate thread

    def stop(self):
        """
        Stop the chat service and close sockets safely.
        """
        self.running = False  # Stop the listener loop
        self.listener.close()
        self.sender.close()
        print("🔻 Chat service stopped.")

# --- Start the chat ---
chat = P2PChat()
chat.start()  # Start listening

while True:
    try:
        msg = input("💬 Enter message: ")  # Get user input
        chat.send(msg)  # Send message to all peers
    except KeyboardInterrupt:
        chat.stop()  # Stop chat when user presses Ctrl+C
        break  # Exit the loop
