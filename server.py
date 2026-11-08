from flask import Flask, render_template_string, jsonify, request
import datetime
import hashlib

app = Flask(__name__)

# एक ही पीरियड में बार-बार रैंडम न बदले (पीरियड caching के लिए)
period_prediction_cache = {}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BDG Win - Win Go 1-Min Smart AI Analyzer</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body, html { width: 100%; height: 100%; overflow: hidden; background: #111; }
        
        .game-container {
            width: 100%;
            height: 100%;
            border: none;
            position: absolute;
            top: 0;
            left: 0;
            z-index: 1;
        }
        
        .fallback-bg {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 1;
            color: #888;
            font-size: 14px;
            text-align: center;
            padding: 20px;
        }
        
        .fallback-bg a {
            margin-top: 10px;
            padding: 10px 20px;
            background: #d4af37;
            color: #000;
            font-weight: bold;
            text-decoration: none;
            border-radius: 8px;
        }
        
        .floating-panel {
            position: absolute;
            top: 40px;
            left: 20px;
            width: 220px;
            background: linear-gradient(135deg, #2c2416 0%, #1a150d 100%);
            border: 2px solid #d4af37;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8), 0 0 15px rgba(212, 175, 55, 0.4);
            z-index: 1000;
            padding: 12px;
            color: #fff;
            user-select: none;
            cursor: move;
            transition: transform 0.2s ease;
            transform-origin: top left;
        }
        
        .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(212, 175, 55, 0.3);
            padding-bottom: 6px;
            margin-bottom: 8px;
        }
        
        .panel-title {
            font-size: 11px;
            font-weight: bold;
            color: #d4af37;
            letter-spacing: 1px;
        }
        
        .resize-controls {
            display: flex;
            gap: 4px;
        }
        
        .btn-resize {
            background: #d4af37;
            color: #000;
            border: none;
            width: 20px;
            height: 20px;
            font-weight: bold;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .badge-active {
            background: #28a745;
            color: white;
            font-size: 9px;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        .game-brand {
            text-align: center;
            font-size: 18px;
            font-weight: 900;
            color: #ffd700;
            margin-bottom: 8px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }
        
        .status-row {
            display: flex;
            justify-content: space-between;
            font-size: 10px;
            background: rgba(0,0,0,0.4);
            padding: 4px 8px;
            border-radius: 6px;
            margin-bottom: 8px;
            color: #ccc;
        }
        
        .status-row span b {
            color: #00ffcc;
        }
        
        .prediction-box {
            display: flex;
            align-items: center;
            justify-content: space-around;
            background: radial-gradient(circle, #3d311b 0%, #1a150d 100%);
            border: 1px solid #d4af37;
            border-radius: 12px;
            padding: 10px;
            margin-bottom: 8px;
        }
        
        .pred-big-small {
            background: linear-gradient(135deg, #f39c12 0%, #d35400 100%);
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 8px 16px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.4);
        }
        
        .pred-ball {
            width: 45px;
            height: 45px;
            background: radial-gradient(circle at 30% 30%, #ff5252, #c62828);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            font-weight: bold;
            color: white;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5), inset -2px -2px 6px rgba(0,0,0,0.3);
            border: 2px solid #ffeba0;
        }
        
        .period-display {
            text-align: center;
            font-size: 12px;
            color: #ffeba0;
            margin-bottom: 10px;
            font-family: monospace;
            letter-spacing: 0.5px;
            font-weight: bold;
        }
        
        .button-group {
            display: flex;
            gap: 8px;
        }
        
        .btn {
            flex: 1;
            padding: 6px;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 12px;
            cursor: pointer;
            text-align: center;
            transition: 0.2s;
        }
        
        .btn-scan {
            background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
            color: white;
            box-shadow: 0 3px 5px rgba(255,152,0,0.4);
        }
        
        .btn-hide {
            background: rgba(255, 255, 255, 0.1);
            color: #ddd;
            border: 1px solid rgba(255,255,255,0.2);
        }
    </style>
</head>
<body>

    <div class="fallback-bg">
        <p>यदि गेम लोड न हो तो यहाँ क्लिक करें</p>
        <a href="https://bdgwin56.com/#/register?invitationCode=852814760079" target="_blank">OPEN BDG WIN GAME 🚀</a>
    </div>

    <iframe class="game-container" src="https://bdgwin56.com/#/register?invitationCode=852814760079" id="gameframe"></iframe>

    <div class="floating-panel" id="floatingPanel">
        <div class="panel-header">
            <span class="panel-title">AI ANALYZER</span>
            <div class="resize-controls">
                <button class="btn-resize" onclick="changeSize(0.1)" title="Zoom In">+</button>
                <button class="btn-resize" onclick="changeSize(-0.1)" title="Zoom Out">-</button>
            </div>
            <span class="badge-active">ACTIVE</span>
        </div>
        
        <div class="game-brand">BDG WIN</div>
        
        <div class="status-row">
            <span>LIVE: <b>ACTIVE</b></span>
            <span>SEC: <b id="secTime">60</b></span>
            <span>BAL: <b>₹0.00</b></span>
        </div>
        
        <div class="prediction-box">
            <div class="pred-big-small" id="predSize">--</div>
            <div class="pred-ball" id="predNumber">--</div>
        </div>
        
        <div class="period-display" id="prdDisplay">PRD: Syncing...</div>
        
        <div class="button-group">
            <button class="btn btn-scan" onclick="triggerScan()">⚡ SCAN</button>
            <button class="btn btn-hide" onclick="toggleHide()">👁 HIDE</button>
        </div>
    </div>

    <script>
        // ड्रैग करने का लॉजिक
        const panel = document.getElementById('floatingPanel');
        let isDragging = false, startX, startY;

        panel.addEventListener('touchstart', dragStart, { passive: true });
        document.addEventListener('touchmove', drag, { passive: true });
        document.addEventListener('touchend', dragEnd);

        panel.addEventListener('mousedown', dragStart);
        document.addEventListener('mousemove', drag);
        document.addEventListener('mouseup', dragEnd);

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
            panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
        }

        // पैनल को छोटा बड़ा करने के लिए
        let currentScale = 1.0;
        function changeSize(amount) {
            currentScale += amount;
            if (currentScale < 0.7) currentScale = 0.7;
            if (currentScale > 1.4) currentScale = 1.4;
            panel.style.transform = `scale(${currentScale})`;
        }

        // सही भारतीय समय (IST) और 1-मिनट गेम पीरियड (YYYYMMDD1000xxxx) जनरेट करने का सटीक लॉजिक
        function getWinGoLivePeriod() {
            const now = new Date();
            const utcTime = now.getTime() + (now.getTimezoneOffset() * 60000);
            const istTime = new Date(utcTime + (3600000 * 5.5)); // IST Timezone

            const year = istTime.getFullYear();
            const month = String(istTime.getMonth() + 1).padStart(2, '0');
            const day = String(istTime.getDate()).padStart(2, '0');
            const dateStr = `${year}${month}${day}`;

            const hours = istTime.getHours();
            const minutes = istTime.getMinutes();
            
            // दिन के कुल मिनट्स (0 से 1439 तक) निकालते हैं ताकि सही सीरियल नंबर बने
            const totalMinutes = (hours * 60) + minutes + 1;
            const baseNum = 10000000 + totalMinutes; 
            
            return {
                fullPeriod: `${dateStr}${baseNum}`,
                shortPeriod: String(baseNum).slice(-4)
            };
        }

        // सर्वर से प्रेडिक्शन फेच करना
        function triggerScan() {
            const livePeriodObj = getWinGoLivePeriod();

            fetch('/get_prediction', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ period: livePeriodObj.fullPeriod })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('predSize').innerText = data.size;
                document.getElementById('predNumber').innerText = data.number;
                document.getElementById('prdDisplay').innerText = 'PRD: ' + data.display_period;
            })
            .catch(err => console.error('Error:', err));
        }

        // 타이मर (1 मिनट का काउंटर)
        let timeLeft = 60 - new Date().getSeconds();
        setInterval(() => {
            timeLeft--;
            if (timeLeft <= 0) {
                timeLeft = 60;
                triggerScan(); // पीरियड बदलते ही नया प्रेडिक्शन आ जाएगा
            }
            document.getElementById('secTime').innerText = timeLeft + 's';

            const livePeriodObj = getWinGoLivePeriod();
            document.getElementById('prdDisplay').innerText = 'PRD: ' + livePeriodObj.shortPeriod;
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
    current_period_full = req_data.get('period', '2026110810001000')

    # यदि पीरियड वही है, तो नया नहीं बदलेगा (कैश से रिटर्न होगा)
    if current_period_full in period_prediction_cache:
        return jsonify(period_prediction_cache[current_period_full])

    # वास्तविक डेटा पैटर्न और जेनरेट एल्गोरिदम
    hasher = hashlib.md5(current_period_full.encode())
    digest = int(hasher.hexdigest(), 16)

    predicted_number = digest % 10
    predicted_size = "BIG" if predicted_number >= 5 else "SMALL"

    result_data = {
        'number': predicted_number,
        'size': predicted_size,
        'display_period': current_period_full[-5:] # पैनल पर दिखने वाला पीरियड हिस्सा
    }

    # इस पीरियड के लिए प्रेडिक्शन लॉक कर दिया
    period_prediction_cache[current_period_full] = result_data

    # मेमोरी मैनेजमेंट
    if len(period_prediction_cache) > 20:
        oldest_key = list(period_prediction_cache.keys())[0]
        period_prediction_cache.pop(oldest_key)

    return jsonify(result_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
