from flask import Flask, render_template, request
import os

app = Flask(__name__)

packets = []

@app.route("/")
def home():
    return render_template("index.html", packets=packets)

@app.route("/start", methods=["POST"])
def start():

    packets.clear()

    num_packets = int(request.form.get("num_packets", 10))

    mock_packets = [
        "192.168.1.10 -> 8.8.8.8 | DNS",
        "192.168.1.15 -> 142.250.183.78 | TCP",
        "192.168.1.20 -> 151.101.1.69 | HTTP",
        "192.168.1.25 -> 172.217.160.78 | HTTPS",
        "192.168.1.30 -> 192.168.1.1 | ARP",
        "192.168.1.35 -> 13.107.21.200 | TCP",
        "192.168.1.40 -> 151.101.65.69 | UDP"
    ]

    for i in range(num_packets):
        packets.append(mock_packets[i % len(mock_packets)])

    return render_template("index.html", packets=packets)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
