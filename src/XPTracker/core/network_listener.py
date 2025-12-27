import threading
import re
from scapy.all import sniff, IP, TCP
from XPTracker.core.input_receiver import InputReceiver


class NetworkListener:
    def __init__(self, input_receiver: InputReceiver):
        self.receiver = input_receiver
        self.target_ip = '18.119.153.121'
        self.target_port = 4000
        self.is_running = False

        # KEY CHANGE 1: A persistent buffer to hold incomplete packet data
        self._buffer = ""

    def remove_noise(self, message):
        """
        Removes ANSI color codes and other noise.
        Matches ESC (x1b) followed by bracket logic.
        """
        # Matches \x1b[...m  (Standard ANSI)
        return re.sub(r'\x1b\[\d+(?:;\d+)*m', '', message)

    def packet_callback(self, packet):
        if IP in packet and TCP in packet:
            if packet[IP].src == self.target_ip and packet[TCP].sport == self.target_port:
                if len(packet[TCP].payload) > 0:
                    try:
                        payload_bytes = bytes(packet[TCP].payload)

                        # KEY CHANGE 2: Decode and IMMEDIATE APPEND to buffer
                        # We do not split yet. We just pile data onto the buffer.
                        chunk = payload_bytes.decode('utf-8', errors='replace')
                        self._buffer += chunk

                        # KEY CHANGE 3: Process buffer looking for complete lines
                        while '\n' in self._buffer:
                            # Split ONLY at the first newline found
                            line, self._buffer = self._buffer.split('\n', 1)

                            # Handle Carriage Returns (\r) usually sent by MUDs
                            line = line.replace('\r', '')

                            # Now we clean the FULL line
                            cleaned = self.remove_noise(line)

                            # Send to app if it has content
                            if cleaned.strip():
                                self.receiver.receive(cleaned)

                    except Exception as e:
                        print(f"Error decoding packet: {e}")

    def start(self):
        self.is_running = True
        print(f"Listening for traffic from {self.target_ip}:{self.target_port}...")
        t = threading.Thread(target=self._sniff_thread, daemon=True)
        t.start()

    def _sniff_thread(self):
        sniff(prn=self.packet_callback, filter="tcp", store=0)