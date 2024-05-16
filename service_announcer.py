import socket
import json
import time
import threading
from peer_discovery import PeerDiscovery

class ServiceAnnouncer:
    def __init__(self):
        self.peer_info = None
        self.username = None
        self.broadcast_ip = "192.168.1.255"
        self.address = None

    def get_broadcast_address(self):
        """
        Attempts to determine the broadcast address for the local network.
        """
        # This is a simplified approach, might need adjustments based on your OS
        ip_address = socket.gethostbyname(socket.gethostname())
        # Split IP address into octets
        ip_octets = ip_address.split(".")
        # Change the last octet to 255 (broadcast)
        ip_octets[-1] = '255'
        # Join octets back into dotted quad format
        self.broadcast_address = ".".join(ip_octets)
        print(self.broadcast_address)
        # print(f"Broadcast address: {self.broadcast_address}")
        return self.broadcast_address


    def get_username(self):
        self.username = input("Please enter your username: ")
        return self.username

    def send_broadcast(self):
        while True:
            data = json.dumps({"username": self.username})
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                sock.sendto(data.encode(), (self.broadcast_ip, 6000))
            time.sleep(8)

    def main(self):
        self.username = self.get_username()
        print(f"Welcome, {self.username}!")
        self.send_broadcast()

    def receive_broadcasts(self):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind((self.broadcast_ip, 6000))  # Listen on port 6000

                data, self.address = sock.recvfrom(1024)
                try:
                    self.peer_info = json.loads(data.decode())
                    self.username = self.peer_info.get("username")
                        # return self.username, self.address[0] # Return the username and IP address of the peer
                    print({"username": self.username})
                except json.JSONDecodeError:
                     print(f"Received invalid broadcast data: {data}")


if __name__ == "__main__":
    announcer = ServiceAnnouncer()
    announcer.main()