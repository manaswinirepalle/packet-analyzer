from flask import Flask, render_template, request, jsonify
from scapy.all import sniff, IP, TCP, UDP, ICMP
import threading
import time
import os
from datetime import datetime

app = Flask(__name__)

packets = []
capturing = False
sniff_thread = None

def packet_callback(pkt):
    """
    Callback function for processing captured packets.
    """
    try:
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
    except Exception as e:
        print(f"Error processing packet: {e}")

def simulate_packets():
    """
    Simulate packet data for testing when real capture fails.
    """
    protocols = ["TCP", "UDP", "ICMP"]
    for i in range(10):
        packet_data = {
            "src_ip": f"192.168.1.{i+1}",
            "dst_ip": f"10.0.0.{i+1}",
            "protocol": protocols[i % 3],
            "size": 100 + i * 10,
            "timestamp": datetime.now().isoformat()
        }
        packets.append(packet_data)
        time.sleep(0.5)  # Simulate delay

def start_capture():
    """
    Starts packet capture or simulation.
    """
    global capturing, sniff_thread
    if not capturing:
        capturing = True
        try:
            sniff_thread = threading.Thread(target=lambda: sniff(prn=packet_callback, store=0, stop_filter=lambda x: not capturing))
            sniff_thread.start()
        except Exception as e:
            print(f"Packet capture failed: {e}. Using simulation.")
            # Fallback to simulation
            sniff_thread = threading.Thread(target=simulate_packets)
            sniff_thread.start()

def stop_capture():
    """
    Stops the capture process.
    """
    global capturing
    capturing = False
    if sniff_thread:
        sniff_thread.join(timeout=1)

@app.route('/')
def home():
    """
    Renders the main dashboard.
    """
    try:
        return render_template("index.html")
    except Exception as e:
        return f"Error loading page: {e}", 500

@app.route('/start_capture', methods=['POST'])
def start_capture_endpoint():
    """
    API endpoint to start capture.
    """
    try:
        start_capture()
        return jsonify({"status": "Capture started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stop_capture', methods=['POST'])
def stop_capture_endpoint():
    """
    API endpoint to stop capture.
    """
    try:
        stop_capture()
        return jsonify({"status": "Capture stopped"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/packets')
def get_packets():
    """
    API endpoint to get packets.
    """
    try:
        return jsonify(packets)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)