from flask import Flask, render_template, request
from scapy.all import *
import threading
import os

app = Flask(__name__)

packets_data = []

def analyze_packet(packet):
    if packet.haslayer(IP):
        packet_info = {
            'src': packet[IP].src,
            'dst': packet[IP].dst,
            'proto': packet[IP].proto
        }
        packets_data.append(packet_info)

@app.route('/')
def index():
    return render_template('index.html', packets=packets_data)

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    global packets_data
    packets_data = []
    count = int(request.form.get('count', 10)) if request.method == 'POST' else 10
    # Run sniff in a thread to avoid blocking
    def sniff_packets():
        sniff(prn=analyze_packet, count=count, store=0)
    thread = threading.Thread(target=sniff_packets)
    thread.start()
    thread.join()  # Wait for completion
    return render_template('index.html', packets=packets_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)