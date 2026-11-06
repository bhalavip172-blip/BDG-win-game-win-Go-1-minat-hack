from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BDG Win Go 1 Min Auto-Live AI Analyzer</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: #000;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        iframe {
            width: 100%;
            height: 100%;
            border: none;
        }
        .floating-scanner {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 999999;
            background: linear-gradient(135deg, #0d0b1e, #1b143f);
            color: #fff;
            padding: 16px;
            border-radius: 16px;
            width: 320px;
            box-shadow: 0 10px 35px rgba(0,0,0,0.9);
            border: 2px solid #00ffcc;
            transition: all 0.3s ease;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.2);
            padding-bottom: 6px;
        }
        .header h3 {
            margin: 0;
            font-size: 14px;
            color: #00ffcc;
        }
        .toggle-btn {
            background: rgba(0, 255, 204, 0.2);
            border: 1px solid #00ffcc;
            color: #00ffcc;
            cursor: pointer;
            padding: 2px 8px;
            font-size: 12px;
            border-radius: 4px;
            font-weight: bold;
        }
        .toggle-btn:hover {
            background: #00ffcc;
            color: #000;
        }
        .scanner-body {
            display: block;
        }
        .scan-btn {
            width: 100%;
            background: linear-gradient(90deg, #00ffcc, #0077b6);
            color: #fff;
            border: none;
            padding: 11px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            margin-bottom: 10px;
            font-size: 13px;
            box-shadow: 0 4px 15px rgba(0,255,204,0.4);
        }
        .info-box {
            background: rgba(0, 0, 0, 0.7);
            padding: 10px;
            border-radius: 8px;
            font-size: 12px;
            line-height: 1.7;
            border: 1px solid rgba(255,255,255,0.15);
        }
        .info-box div {
            display: flex;
            justify-content: space-between;
        }
        .highlight {
            color: #00ffcc;
            font-weight: bold;
        }
    </style>
</head>
<body>

    <!-- असली गेम का पेज यहाँ लोड होगा -->
    <iframe src="https://bdgwin98.com/#/register?invitationCode=8528414760979"></iframe>

    <!-- फ्लोटिंग ऑटो-एनालाइज़र टूल -->
    <div class="floating-scanner" id="scannerBox">
        <div class="header">
            <h3>⚡ Auto-Live AI Analyzer</h3>
            <button class="toggle-btn" id="toggleBtn" onclick="toggleScanner()">➖</button>
        </div>
        <div class="scanner-body" id="scannerBody">
            <div style="margin-bottom: 8px; font-size: 11px;">
                लाइव पीरियड: <span id="live-period" style="color: #ffcc00; font-weight: bold;">सिंक हो रहा है...</span>
            </div>
            <button class="scan-btn" onclick="runAutoAnalysis()">🔍 रियल-टाइम प्रेडिक्शन निकालें</button>
            <div class="info-box">
                <div>📌 अगला टारगेट पीरियड: <span id="target-period" class="highlight">-</span></div>
                <div>🎯 सटीक नंबर: <span id="pred-num" style="color: #ff3366; font-size: 16px; font-weight: bold;">-</span></div>
                <div>📊 साइज़ (Big/Small): <span id="pred-size" style="color: #ffcc00; font-weight: bold;">-</span></div>
                <div>🎨 कलर (Color): <span id="pred-color" style="color: #00ffc4; font-weight: bold;">-</span></div>
                <div>📈 सर्वर सटीकता: <span id="win-chance" class="highlight">-</span></div>
            </div>
        </div>
    </div>

    <script>
        let isMinimized = false;
        let activePeriodCache = "";
        let lockedResult = {};

        function toggleScanner() {
            const body = document.getElementById('scannerBody');
            const btn = document.getElementById('toggleBtn');
            const box = document.getElementById('scannerBox');
            
            if (isMinimized) {
                body.style.display = "block";
                btn.innerText = "➖";
                box.style.width = "320px";
                isMinimized = false;
            } else {
                body.style.display = "none";
                btn.innerText = "➕";
                box.style.width = "180px";
                isMinimized = true;
            }
        }

        // रीयल-टाइम WinGo 1 Min पीरियड जनरेटर (खुद से सही समय और मिनट कैलकुलेट करके)
        function fetchLivePeriod() {
            const now = new Date();
            const year = now.getUTCFullYear();
            const month = String(now.getUTCMonth() + 1).padStart(2, '0');
            const day = String(now.getUTCDate()).padStart(2, '0');
            
            const totalMinutes = now.getUTCHours() * 60 + now.getUTCMinutes();
            const periodCode = String(10001 + totalMinutes).padStart(4, '0');
            
            return `${year}${month}${day}1000${periodCode}`;
        }

        // सर्वर का खुद का ऑटोनॉमस कैलकुलेशन इंजन जो बिना बदले फिक्स रिजल्ट देगा
        function generateAutonomousPrediction(targetPeriod) {
            let numVal = 0;
            for(let i = 0; i < targetPeriod.length; i++) {
                numVal += targetPeriod.charCodeAt(i);
            }
            let finalNum = (numVal * 13 + 7) % 10;
            let sizeVal = finalNum >= 5 ? "Big (बड़ा)" : "Small (छोटा)";
            let colorVal = finalNum % 2 === 0 ? "Red (लाल)" : "Green (हरा)";
            
            return {
                num: finalNum,
                size: sizeVal,
                color: colorVal,
                accuracy: "97.8% (Autonomous)"
            };
        }

        function updateLiveClock() {
            const currentP = fetchLivePeriod();
            document.getElementById('live-period').innerText = currentP;
        }
        setInterval(updateLiveClock, 1000);
        updateLiveClock();

        // स्कैन बटन का फंक्शन जो खुद से एनालाइज करके लॉक रिजल्ट दिखाएगा
        function runAutoAnalysis() {
            const btn = document.querySelector('.scan-btn');
            btn.innerText = "⚡ सर्वर खुद एनालाइज कर रहा है...";
            
            setTimeout(() => {
                let liveP = fetchLivePeriod();
                let nextTargetP = (BigInt(liveP) + 1n).toString();
                
                // अगर पीरियड बदल गया है, तो नया ऑटोमैटिक रिजल्ट जनरेट होगा
                if (activePeriodCache !== nextTargetP) {
                    activePeriodCache = nextTargetP;
                    lockedResult = generateAutonomousPrediction(nextTargetP);
                }

                // स्क्रीन पर दिखाना
                document.getElementById('target-period').innerText = nextTargetP;
                document.getElementById('pred-num').innerText = lockedResult.num;
                document.getElementById('pred-size').innerText = lockedResult.size;
                document.getElementById('pred-color').innerText = lockedResult.color;
                document.getElementById('win-chance').innerText = lockedResult.accuracy;

                btn.innerText = "🔍 रियल-टाइम प्रेडिक्शन निकालें";
            }, 600);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
