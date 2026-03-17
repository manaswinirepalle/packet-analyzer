from flask import Flask, render_template, request, jsonify
from scapy.all import sniff, IP, TCP, UDP, ICMP
import threading
import time
from datetime import datetime

app = Flask(__name__)

packets = []
capturing = False
sniff_thread = None

def packet_callback(pkt):
    if IP in pkt:
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        size = len(pkt)
        timestamp = datetime.now().isoformat()
        
        protocol = "Unknown"
        if TCP in pkt:
            protocol = "TCP"
        elif UDP in pkt:
            protocol = "UDP"
        elif ICMP in pkt:
            protocol = "ICMP"
        
        packet_data = {
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "protocol": protocol,
            "size": size,
            "timestamp": timestamp
        }
        packets.append(packet_data)

def start_capture():
    global capturing, sniff_thread
    if not capturing:
        capturing = True
        sniff_thread = threading.Thread(target=lambda: sniff(prn=packet_callback, store=0, stop_filter=lambda x: not capturing))
        sniff_thread.start()

def stop_capture():
    global capturing
    capturing = False
    if sniff_thread:
        sniff_thread.join(timeout=1)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/start_capture', methods=['POST'])
def start_capture_endpoint():
    start_capture()
    return jsonify({"status": "Capture started"})

@app.route('/stop_capture', methods=['POST'])
def stop_capture_endpoint():
    stop_capture()
    return jsonify({"status": "Capture stopped"})

@app.route('/packets')
def get_packets():
    return jsonify(packets)

if __name__ == "__main__":
    app.run(debug=True)