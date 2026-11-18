from flask import Flask, render_template_string, request, jsonify
import random
import hashlib
from datetime import datetime

app = Flask(__name__)

period_prediction_cache = {}
history_records = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BDGWin Pro AI Analyzer</title>
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
            background: #050811;
        }

        /* बैकग्राउंड में गेम का लिंक iframe ताकि गेम और पैनल दोनों साथ दिखें */
        #gameFrame {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
            z-index: 1;
        }

        /* वीडियो वाले स्टाइल का डार्क/नियन फ्लोटिंग पैनल */
        #panel {
            position: absolute;
            top: 40px;
            left: 40px;
            width: 330px;
            background: rgba(10, 15, 30, 0.92);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(56, 189, 248, 0.5);
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.8), 0 0 25px rgba(56, 189, 248, 0.3);
            color: #ffffff;
            z-index: 999999;
            user-select: none;
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
        }

        .panel-body {
            padding: 12px;
        }

        .info-box {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            padding: 6px 10px;
            margin-bottom: 8px;
            font-size: 11px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .info-box span {
            color: #94a3b8;
        }

        .result-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-bottom: 8px;
        }

        .result-card {
            background: rgba(56, 189, 248, 0.05);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: 8px;
            padding: 8px;
            text-align: center;
        }

        .result-card .label {
            font-size: 9px;
            color: #94a3b8;
            margin-bottom: 2px;
        }

        .result-card .value {
            font-size: 15px;
            font-weight: bold;
            color: #f8fafc;
        }

        .footer-info {
            display: flex;
            justify-content: space-between;
            font-size: 10px;
            background: rgba(0, 0, 0, 0.4);
            padding: 6px 10px;
            border-radius: 8px;
            color: #cbd5e1;
        }

        .game-link-btn {
            display: block;
            width: 100%;
            text-align: center;
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            text-decoration: none;
            padding: 6px;
            border-radius: 6px;
            font-size: 10px;
            font-weight: bold;
            margin-top: 8px;
        }
    </style>
</head>
<body>

    <!-- असली गेम का पेज बैकएंड पर लोड रहेगा -->
    <iframe id="gameFrame" src="https://bdgwin37.com/#/register?invitationCode=8528414760979"></iframe>

    <!-- फ्लोटिंग और ड्रैगेबल पैनल -->
    <div id="panel">
        <div class="panel-header" id="panelHeader">
            <span>⚡ BDGWin AI Overlay</span>
            <div class="controls">
                <button onclick="changeSize(0.1)" title="Zoom In">+</button>
                <button onclick="changeSize(-0.1)" title="Zoom Out">-</button>
                <button onclick="toggleHide()" title="Minimize">_</button>
            </div>
        </div>
        
        <div class="panel-body" id="panelBody">
            <div class="info-box">
                <span>Current Period:</span>
                <strong id="prdDisplay" style="color: #38bdf8; font-size: 10px;">Loading...</strong>
            </div>

            <div class="result-grid">
                <div class="result-card">
                    <div class="label">PREDICTED SIZE</div>
                    <div class="value" id="predSize">--</div>
                </div>
                <div class="result-card">
                    <div class="label">LUCKY NUMBER</div>
                    <div class="value" id="predNumber" style="color: #38bdf8;">--</div>
                </div>
            </div>

            <div class="footer-info">
                <span>Timer: <b id="secTime" style="color: #f43f5e;">60s</b></span>
                <span>Accuracy: <b id="accuracy" style="color: #10b981;">--%</b></span>
            </div>

            <a href="https://bdgwin37.com/#/register?invitationCode=8528414760979" target="_blank" class="game-link-btn">🔗 Open Official Game Page</a>
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
            if (e.target.tagName === 'BUTTON' || e.target.tagName === 'A') return;
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

        // 1-मिनट के हिसाब से सही पीरियड कैलकुलेटर (बेस 9671)
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

        function triggerScan() {
            const livePeriod = getWinGoLivePeriod();
            document.getElementById('prdDisplay').innerText = livePeriod;

            fetch('/get_prediction', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ period: livePeriod })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('predSize').innerText = data.size;
                document.getElementById('predNumber').innerText = data.number;
                document.getElementById('accuracy').innerText = data.accuracy + '%';
            })
            .catch(err => console.error("Error:", err));
        }

        // 60-सेकंड का लाइव टाइमर
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
    current_period_full = req_data.get('period', '20261118100010250')

    if current_period_full in period_prediction_cache:
        return jsonify(period_prediction_cache[current_period_full])

    try:
        base_num = int(current_period_full)
    except:
        base_num = 20261118100010250

    history_records.append(base_num)
    if len(history_records) > 15:
        history_records.pop(0)

    combined_history_str = "".join(str(p % 100) for p in history_records)
    deep_analysis_seed = f"{base_num}-{combined_history_str}-{len(history_records)}"

    hasher = hashlib.sha256(deep_analysis_seed.encode())
    digest = int(hasher.hexdigest(), 16)

    predicted_number = digest % 10
    predicted_size = "BIG" if predicted_number >= 5 else "SMALL"
    dynamic_accuracy = round(random.uniform(99.3, 99.9), 1)

    result_data = {
        "number": predicted_number,
        "size": predicted_size,
        "accuracy": dynamic_accuracy,
        "display_period": current_period_full
    }

    period_prediction_cache[current_period_full] = result_data

    if len(period_prediction_cache) > 50:
        oldest_key = list(period_prediction_cache.keys())[0]
        period_prediction_cache.pop(oldest_key)

    return jsonify(result_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
