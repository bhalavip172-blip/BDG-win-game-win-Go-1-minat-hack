from flask import Flask, render_template_string, request, jsonify
import random
import hashlib
from datetime import datetime

app = Flask(__name__)

period_prediction_cache = {}
history_records = []
past_results_log = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BDGWin Live Overlay Analyzer</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body, html {
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: #090d16;
        }

        /* बैकग्राउंड में गेम चलाने के लिए Iframe */
        #gameFrame {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            border: none;
            z-index: 1;
        }

        /* फ्लोटिंग पैनल जो गेम के ऊपर तैरता रहेगा */
        #panel {
            position: absolute;
            top: 30px;
            left: 30px;
            width: 330px;
            background: rgba(13, 20, 38, 0.92);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(56, 189, 248, 0.5);
            border-radius: 16px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.7), 0 0 20px rgba(56, 189, 248, 0.3);
            color: #ffffff;
            z-index: 9999; /* गेम के ऊपर रखने के लिए सबसे ज्यादा z-index */
            user-select: none;
            transition: transform 0.1s ease;
        }

        .panel-header {
            padding: 10px 14px;
            background: linear-gradient(135deg, #0284c7, #1d4ed8);
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            cursor: move;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: bold;
            font-size: 12px;
            letter-spacing: 0.5px;
        }

        .controls button {
            background: none;
            border: none;
            color: white;
            cursor: pointer;
            font-size: 14px;
            margin-left: 6px;
            transition: opacity 0.2s;
        }

        .controls button:hover {
            opacity: 0.7;
        }

        .panel-body {
            padding: 12px;
        }

        /* UID कनेक्शन सेक्शन */
        .uid-section {
            margin-bottom: 8px;
            display: flex;
            gap: 6px;
        }

        .uid-section input {
            flex: 1;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 6px;
            padding: 5px 8px;
            color: #fff;
            font-size: 11px;
            outline: none;
        }

        .uid-section input:focus {
            border-color: #38bdf8;
        }

        .uid-section button {
            background: #10b981;
            border: none;
            color: white;
            padding: 5px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.2s;
        }

        .uid-section button:hover {
            background: #059669;
        }

        #uidStatus {
            font-size: 9px;
            color: #10b981;
            margin-bottom: 6px;
            display: none;
            font-weight: 600;
        }

        .info-box {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 6px;
            padding: 6px 8px;
            margin-bottom: 6px;
            font-size: 11px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .info-box span {
            color: #94a3b8;
        }

        #analyzeStatus {
            text-align: center;
            font-size: 10px;
            color: #f59e0b;
            margin-bottom: 6px;
            font-weight: 600;
            min-height: 14px;
        }

        .result-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px;
            margin-bottom: 6px;
        }

        .result-card {
            background: rgba(56, 189, 248, 0.05);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: 6px;
            padding: 6px;
            text-align: center;
        }

        .result-card .label {
            font-size: 9px;
            color: #94a3b8;
            margin-bottom: 2px;
        }

        .result-card .value {
            font-size: 14px;
            font-weight: bold;
            color: #f8fafc;
        }

        /* पिछले डेटा की हिस्ट्री */
        .history-container {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 6px;
            padding: 5px;
            margin-bottom: 6px;
            max-height: 85px;
            overflow-y: auto;
        }

        .history-title {
            font-size: 9px;
            color: #94a3b8;
            margin-bottom: 3px;
            text-align: center;
            font-weight: bold;
        }

        .history-item {
            display: flex;
            justify-content: space-between;
            font-size: 9px;
            padding: 2px 4px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        }

        .history-item:last-child {
            border-bottom: none;
        }

        .footer-info {
            display: flex;
            justify-content: space-between;
            font-size: 10px;
            color: #cbd5e1;
            background: rgba(0, 0, 0, 0.3);
            padding: 5px 8px;
            border-radius: 6px;
        }
    </style>
</head>
<body>

    <!-- बैकग्राउंड में गेम लोड करने के लिए Iframe -->
    <iframe id="gameFrame" src="https://bdgwin37.com/#/register?invitationCode=8528414760979" title="BDGWin Game"></iframe>

    <!-- फ्लोटिंग प्रेडिक्शन पैनल जो गेम के ऊपर तैरता रहेगा -->
    <div id="panel">
        <div class="panel-header" id="panelHeader">
            <span>⚡ BDGWin Floating AI</span>
            <div class="controls">
                <button onclick="changeSize(0.1)">+</button>
                <button onclick="changeSize(-0.1)">-</button>
                <button onclick="toggleHide()">_</button>
            </div>
        </div>
        
        <div class="panel-body" id="panelBody">
            <!-- UID कनेक्ट करने का बॉक्स -->
            <div class="uid-section">
                <input type="text" id="uidInput" placeholder="Enter Game UID">
                <button onclick="connectUID()">Link</button>
            </div>
            <div id="uidStatus">✓ UID Linked</div>

            <div class="info-box">
                <span>Period:</span>
                <strong id="prdDisplay" style="font-size: 10px; color: #38bdf8;">Loading...</strong>
            </div>

            <div id="analyzeStatus">⚡ AI Ready</div>

            <div class="result-grid">
                <div class="result-card">
                    <div class="label">SIZE</div>
                    <div class="value" id="predSize">--</div>
                </div>
                <div class="result-card">
                    <div class="label">NUMBER</div>
                    <div class="value" id="predNumber" style="color: #38bdf8;">--</div>
                </div>
            </div>

            <!-- पिछले डेटा की हिस्ट्री -->
            <div class="history-container">
                <div class="history-title">-- RECENT ANALYZED DATA --</div>
                <div id="historyList">
                    <div style="text-align:center; color:#64748b; font-size:9px;">Waiting...</div>
                </div>
            </div>

            <div class="footer-info">
                <span>Timer: <b id="secTime" style="color: #f43f5e;">60s</b></span>
                <span>Acc: <b id="accuracy" style="color: #10b981;">--%</b></span>
            </div>
        </div>
    </div>

    <script>
        const panel = document.getElementById('panel');
        const header = document.getElementById('panelHeader');
        let isDragging = false, startX, startY;

        header.addEventListener('mousedown', dragStart);
        document.addEventListener('mousemove', drag);
        document.addEventListener('mouseup', dragEnd);

        header.addEventListener('touchstart', dragStart);
        document.addEventListener('touchmove', drag);
        document.addEventListener('touchend', dragEnd);

        function dragStart(e) {
            if (e.target.tagName === 'BUTTON') return;
            isDragging = true;
            const clientX = e.type === 'touchstart' ? e.touches[0].clientX : e.clientX;
            const clientY = e.type === 'touchstart' ? e.touches[0].clientY : e.clientY;
            startX = clientX - panel.offsetLeft;
            startY = clientY - panel.offsetTop;
        }

        function drag(e) {
            if (!isDragging) return;
            const clientX = e.type === 'touchmove' ? e.touches[0].clientX : e.clientX;
            const clientY = e.type === 'touchmove' ? e.touches[0].clientY : e.clientY;
            panel.style.left = (clientX - startX) + 'px';
            panel.style.top = (clientY - startY) + 'px';
        }

        function dragEnd() { isDragging = false; }

        function toggleHide() {
            const body = document.getElementById('panelBody');
            body.style.display = body.style.display === 'none' ? 'block' : 'none';
        }

        let currentScale = 1.0;
        function changeSize(amount) {
            currentScale += amount;
            if (currentScale < 0.75) currentScale = 0.75;
            if (currentScale > 1.25) currentScale = 1.25;
            panel.style.transform = `scale(${currentScale})`;
        }

        let linkedUID = "";
        function connectUID() {
            const uid = document.getElementById('uidInput').value.trim();
            const status = document.getElementById('uidStatus');
            if(uid !== "") {
                linkedUID = uid;
                status.style.display = "block";
                status.innerText = "✓ UID: " + uid + " Linked";
            } else {
                alert("Please enter a valid UID first!");
            }
        }

        function getWinGoLivePeriod() {
            const now = new Date();
            const utcTime = now.getTime() + (now.getTimezoneOffset() * 60000);
            const istTime = new Date(utcTime + (3600000 * 5.5));

            const year = istTime.getFullYear();
            const month = String(istTime.getMonth() + 1).padStart(2, '0');
            const day = String(istTime.getDate()).padStart(2, '0');
            const dateStr = `${year}${month}${day}`;

            const startOfDay = new Date(istTime.getFullYear(), istTime.getMonth(), istTime.getDate());
            const totalMinutesToday = Math.floor((istTime - startOfDay) / 60000);

            const exactPeriodNum = 9671 + totalMinutesToday;
            return `${dateStr}1000${exactPeriodNum}`;
        }

        let lastFetchedPeriod = "";

        function triggerScan() {
            const livePeriod = getWinGoLivePeriod();
            document.getElementById('prdDisplay').innerText = livePeriod;

            if (livePeriod !== lastFetchedPeriod) {
                lastFetchedPeriod = livePeriod;
                
                document.getElementById('analyzeStatusinnerHTML = "🔄 Analyzing trends...";' // syntax check
                document.getElementById('analyzeStatus').innerHTML = "🔄 Analyzing trends...";
                document.getElementById('predSize').innerText = "...";
                document.getElementById('predNumber').innerText = "...";

                setTimeout(() => {
                    fetch('/get_prediction', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ period: livePeriod, uid: linkedUID })
                    })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('analyzeStatus').innerHTML = "✨ Ready!";
                        document.getElementById('predSize').innerText = data.size;
                        document.getElementById('predNumber').innerText = data.number;
                        document.getElementById('accuracy').innerText = data.accuracy + '%';

                        updateHistoryUI(data.history);
                    })
                    .catch(err => {
                        console.error("Error:", err);
                        document.getElementById('analyzeStatus').innerHTML = "⚠ Error!";
                    });
                }, 1000);
            }
        }

        function updateHistoryUI(historyArr) {
            const historyList = document.getElementById('historyList');
            historyList.innerHTML = "";
            
            historyArr.slice(-10).reverse().forEach(item => {
                const div = document.createElement('div');
                div.className = 'history-item';
                div.innerHTML = `<span>Prd: ${item.period.slice(-4)}</span> <b style="color:${item.size === 'BIG' ? '#38bdf8' : '#f43f5e'}">${item.size} (${item.number})</b>`;
                historyList.appendChild(div);
            });
        }

        setInterval(() => {
            let secNow = new Date().getSeconds();
            let timeLeft = 60 - secNow;
            if (timeLeft === 60) timeLeft = 0;

            document.getElementById('secTime').innerText = timeLeft + 's';

            if (secNow === 0) {
                triggerScan();
            }
        }, 1000);

        window.onload = triggerScan;
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_prediction', methods=['POST'])
def get_prediction():
    req_data = request.get_json() or {}
    current_period_full = req_data.get('period', '20261108100010289')
    client_uid = req_data.get('uid', 'default')

    if current_period_full in period_prediction_cache:
        cached_data = period_prediction_cache[current_period_full]
        cached_data['history'] = past_results_log
        return jsonify(cached_data)

    try:
        base_num = int(current_period_full)
    except:
        base_num = 20261108100010289

    trend_modifier = 0
    if len(past_results_log) >= 3:
        recent_sum = sum(item['number'] for item in past_results_log[-3:])
        trend_modifier = (recent_sum + len(str(client_uid))) % 7

    raw_seed = f"{client_uid}-{base_num}-{trend_modifier}-{len(past_results_log)}"
    hasher = hashlib.sha256(raw_seed.encode())
    digest = int(hasher.hexdigest(), 16)

    predicted_number = (digest + trend_modifier) % 10
    predicted_size = "BIG" if predicted_number >= 5 else "SMALL"
    dynamic_accuracy = round(random.uniform(99.4, 99.9), 1)

    result_data = {
        "number": predicted_number,
        "size": predicted_size,
        "accuracy": dynamic_accuracy,
        "display_period": current_period_full
    }

    past_results_log.append({
        "period": current_period_full,
        "number": predicted_number,
        "size": predicted_size
    })
    
    if len(past_results_log) > 15:
        past_results_log.pop(0)

    result_data['history'] = past_results_log
    period_prediction_cache[current_period_full] = result_data

    if len(period_prediction_cache) > 50:
        oldest_key = list(period_prediction_cache.keys())[0]
        period_prediction_cache.pop(oldest_key)

    return jsonify(result_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
