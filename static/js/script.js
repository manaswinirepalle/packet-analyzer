document.addEventListener('DOMContentLoaded', function() {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const packetTable = document.getElementById('packetTable');
    const searchInput = document.getElementById('searchInput');
    const protocolFilter = document.getElementById('protocolFilter');
    const totalPacketsEl = document.getElementById('totalPackets');
    const tcpPacketsEl = document.getElementById('tcpPackets');
    const udpPacketsEl = document.getElementById('udpPackets');

    let packets = [];
    let filteredPackets = [];

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Chart
    const ctx = document.getElementById('protocolChart').getContext('2d');
    const protocolChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['TCP', 'UDP', 'ICMP', 'Other'],
            datasets: [{
                data: [0, 0, 0, 0],
                backgroundColor: ['#ffc107', '#17a2b8', '#dc3545', '#6c757d']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Protocol Distribution'
                }
            }
        }
    });

    // Start capture
    startBtn.addEventListener('click', function() {
        fetch('/start_capture', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                alert(data.status);
                startBtn.disabled = true;
                stopBtn.disabled = false;
            });
    });

    // Stop capture
    stopBtn.addEventListener('click', function() {
        fetch('/stop_capture', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                alert(data.status);
                startBtn.disabled = false;
                stopBtn.disabled = true;
            });
    });

    // Fetch packets periodically
    setInterval(fetchPackets, 2000);

    function fetchPackets() {
        fetch('/packets')
            .then(response => response.json())
            .then(data => {
                packets = data;
                updateDisplay();
            });
    }

    function updateDisplay() {
        // Filter packets
        filteredPackets = packets.filter(packet => {
            const matchesSearch = searchInput.value === '' || 
                packet.src_ip.includes(searchInput.value) || 
                packet.dst_ip.includes(searchInput.value);
            const matchesProtocol = protocolFilter.value === '' || packet.protocol === protocolFilter.value;
            return matchesSearch && matchesProtocol;
        });

        // Update table
        packetTable.innerHTML = '';
        filteredPackets.forEach(packet => {
            const row = document.createElement('tr');
            if (packet.protocol === 'ICMP') {
                row.classList.add('table-warning'); // Highlight suspicious
            }
            row.innerHTML = `
                <td>${packet.timestamp}</td>
                <td>${packet.src_ip}</td>
                <td>${packet.dst_ip}</td>
                <td>${packet.protocol}</td>
                <td>${packet.size}</td>
            `;
            packetTable.appendChild(row);
        });

        // Update stats
        totalPacketsEl.textContent = packets.length;
        const tcpCount = packets.filter(p => p.protocol === 'TCP').length;
        const udpCount = packets.filter(p => p.protocol === 'UDP').length;
        const icmpCount = packets.filter(p => p.protocol === 'ICMP').length;
        const otherCount = packets.length - tcpCount - udpCount - icmpCount;

        tcpPacketsEl.textContent = tcpCount;
        udpPacketsEl.textContent = udpCount;

        protocolChart.data.datasets[0].data = [tcpCount, udpCount, icmpCount, otherCount];
        protocolChart.update();
    }

    // Event listeners for filters
    searchInput.addEventListener('input', updateDisplay);
    protocolFilter.addEventListener('change', updateDisplay);
});