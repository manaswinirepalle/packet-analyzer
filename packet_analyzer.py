from flask import Flask, render_template
import random

app = Flask(__name__)

# Mock packet data for demo
mock_packets = [
    "Ether / IP / TCP 192.168.1.1:80 > 192.168.1.2:12345",
    "Ether / IP / UDP 10.0.0.1:53 > 10.0.0.2:5353",
    "Ether / IP / ICMP 172.16.0.1 > 172.16.0.2",
    "Ether / ARP who has 192.168.1.2 says 192.168.1.1",
    "Ether / IP / TCP 192.168.1.2:12345 > 192.168.1.1:80"
]

packets = []

@app.route('/')
def home():
    return render_template("index.html", packets=packets)

@app.route('/start')
def start():
    # Generate mock packets instead of real sniffing
    packets.clear()
    for _ in range(random.randint(5, 15)):
        packets.append(random.choice(mock_packets))
    return render_template("index.html", packets=packets)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
